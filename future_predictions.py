import numpy as np
import pandas as pd
import plotly.graph_objects as go
from DataPreprocessing.data_preprocessing import preprocess_data
from model_architecture.model_architecture import create_lstm_tensors, build_lstm_model
from sklearn.preprocessing import MinMaxScaler
import torch

def generate_predictions():

    EXCEL_FILE_PATH = "Stored_data/cleaned_data.xlsx"
    data = pd.read_excel(EXCEL_FILE_PATH)
    
    # Ensure the data contains the required columns: Date, Open, High, Low, Close
    print(f"Columns: {data.columns}")
    
    # Preprocess the data
    preprocessed_data, scaler = preprocess_data(data)
    
    # Extract 'Close' prices and other OHLC values for scaling
    close_prices = preprocessed_data['Close'].values
    
    # Fit the MinMaxScaler only on the 'Close' prices
    close_scaler = MinMaxScaler(feature_range=(0, 1))
    close_scaler.fit(close_prices.reshape(-1, 1))
    
    # Scale the close prices
    scaled_close_prices = close_scaler.transform(close_prices.reshape(-1, 1))
    
    # Remove the 'Close' feature from the input data
    input_features = preprocessed_data.drop('Close', axis=1)
    
    # Create LSTM tensors
    window_size = 35
    lstm_input = create_lstm_tensors(input_features, window_size)
    
    # Print shape of lstm_input for verification
    print(f"Shape of lstm_input: {lstm_input.shape}")  # (num_samples, window_size, input_dim)
    
    # Define the number of days for future predictions
    x_days = 30  # 30-day future predictions on a daily basis
    
    # Prepare the last window of data for prediction
    # Convert to NumPy array and reshape to (1, window_size, input_dim)
    last_data = lstm_input[-1, :, :].numpy()  # Shape: (window_size, input_dim)
    last_data = last_data[np.newaxis, :, :]  # Shape: (1, window_size, input_dim)
    
    # Build and load the model once
    model = build_lstm_model(lstm_input)
    try:
        model.load_state_dict(torch.load('Stored_data/lstm_model.pt', weights_only=True))
    except TypeError:
        # If weights_only is not supported (older PyTorch versions), omit the argument
        model.load_state_dict(torch.load('Stored_data/lstm_model.pt'))
    model.eval()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    # Make predictions for the next x_days
    predictions = []
    with torch.no_grad():
        for day in range(x_days):
            # Convert last_data to tensor and send to device
            last_data_tensor = torch.FloatTensor(last_data).to(device)
            
            # Make prediction
            predicted_price_tensor = model(last_data_tensor)
            predicted_price = predicted_price_tensor.cpu().numpy()[0, 0]
            predictions.append(predicted_price)
            
            # Update the input window for the next prediction
            # Shift window left by 1
            last_data = np.roll(last_data, -1, axis=1)  # Shift window left by 1
            
            # Update only the 'Close' feature (assuming it's the first feature)
            # Adjust the index if 'Close' is in a different position
            last_data[0, -1, 0] = predicted_price  # Example: 'Close' is at index 0
            
            # No need to convert back to tensor here; it will be converted in the next iteration
            
    # Create a date range for the future predictions (daily)
    last_date = pd.to_datetime(data['Date'].iloc[-1])
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=x_days, freq='D')
    
    # Create a DataFrame for predictions
    predictions_df = pd.DataFrame({
        'Date': future_dates,
        'Predicted Close': predictions
    })
    
    # Inverse transform the predicted prices
    predictions_df['Predicted Close'] = close_scaler.inverse_transform(predictions_df[['Predicted Close']])
    
    # For simplicity, we'll assume constant Open, High, Low for predicted values (can be customized)
    predictions_df['Predicted Open'] = predictions_df['Predicted Close'] * 0.99  # Example assumption: Open is 1% lower
    predictions_df['Predicted High'] = predictions_df['Predicted Close'] * 1.02  # Example assumption: High is 2% higher
    predictions_df['Predicted Low'] = predictions_df['Predicted Close'] * 0.98  # Example assumption: Low is 2% lower
    
    return predictions_df, data

def plot_predictions(predictions_df, data):
    # Plot using Plotly Candlestick chart
    fig = go.Figure()
    
    # Add historical candlestick data (OHLC)
    fig.add_trace(go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Historical Prices'
    ))
    
    # Add predicted candlestick data (OHLC)
    fig.add_trace(go.Candlestick(
        x=predictions_df['Date'],
        open=predictions_df['Predicted Open'],
        high=predictions_df['Predicted High'],
        low=predictions_df['Predicted Low'],
        close=predictions_df['Predicted Close'],
        name='Predicted Prices',
        increasing_line_color='orange',
        decreasing_line_color='red',
        opacity=0.6  # Make predicted candles slightly transparent
    ))
    
    # Customize layout for better scrollability and interaction
    fig.update_layout(
        title='Bitcoin Price Prediction (Candlestick)',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=True,  # Enable the range slider
        xaxis_type='date',
        hovermode="x unified",
        template='plotly_dark'  # Optional: Dark theme
    )
    
    # Show the plot
    fig.show()

# If you want to run this script standalone for testing:
if __name__ == "__main__":
    predictions_df, data = generate_predictions()
    plot_predictions(predictions_df, data)
