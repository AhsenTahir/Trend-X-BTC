import numpy as np
import pandas as pd
import plotly.graph_objects as go
from DataPreprocessing.data_preprocessing import preprocess_data
from model_architecture.model_architecture import create_lstm_tensors, build_lstm_model
from sklearn.preprocessing import MinMaxScaler
import torch
from firebase_utils import save_df_to_firebase, load_df_from_firebase, file_exists_in_firebase, load_model_from_firebase

def generate_predictions():
    try:
        # Load data from Firebase first, fall back to local if needed
        if file_exists_in_firebase('data/cleaned_data.csv'):
            data = load_df_from_firebase('cleaned_data.csv')
            print("Loaded data from Firebase Storage")
        else:
            data = pd.read_excel("Stored_data/cleaned_data.xlsx")
            print("Loaded data from local Excel file")
        
        # Ensure the data contains the required columns
        print(f"Columns: {data.columns}")
        
        # Preprocess the data
        preprocessed_data, scaler = preprocess_data(data)
        
        # Extract 'Close' prices and other OHLC values for scaling
        close_prices = preprocessed_data['Close'].values
        
        # Fit the MinMaxScaler only on the 'Close' prices
        close_scaler = MinMaxScaler(feature_range=(0, 1))
        close_scaler.fit(close_prices.reshape(-1, 1))
        
        # Create LSTM tensors and make predictions
        input_features = preprocessed_data.drop('Close', axis=1)
        window_size = 35
        lstm_input = create_lstm_tensors(input_features, window_size)
        
        # Build model and load weights from Firebase if available
        model = build_lstm_model(lstm_input)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        
        if file_exists_in_firebase('models/lstm_model.pt'):
            try:
                model = load_model_from_firebase(lambda: build_lstm_model(lstm_input), 'lstm_model.pt')
                print("Loaded model from Firebase Storage")
            except Exception as e:
                print(f"Error loading model from Firebase: {e}")
                model.load_state_dict(torch.load('Stored_data/lstm_model.pt'))
                print("Loaded model from local storage")
        else:
            model.load_state_dict(torch.load('Stored_data/lstm_model.pt'))
            print("Loaded model from local storage")
        
        model.eval()
        
        # Generate predictions
        x_days = 30
        predictions = []
        last_data = lstm_input[-1, :, :].numpy()[np.newaxis, :, :]
        
        with torch.no_grad():
            for _ in range(x_days):
                last_data_tensor = torch.FloatTensor(last_data).to(device)
                predicted_price = model(last_data_tensor).cpu().numpy()[0, 0]
                predictions.append(predicted_price)
                last_data = np.roll(last_data, -1, axis=1)
                last_data[0, -1, 0] = predicted_price
        
        # Create predictions DataFrame
        last_date = pd.to_datetime(data['Date'].iloc[-1])
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=x_days, freq='D')
        
        predictions_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted Close': close_scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
        })
        
        # Add other price predictions
#        predictions_df['Predicted Open'] = predictions_df['Predicted Close'] * 0.99
#        predictions_df['Predicted High'] = predictions_df['Predicted Close'] * 1.02
#        predictions_df['Predicted Low'] = predictions_df['Predicted Close'] * 0.98
        
        # Save predictions both locally and to Firebase
        predictions_df.to_excel('Stored_data/predictions.xlsx', index=False)
        save_df_to_firebase(predictions_df, 'predictions.csv')  # Save to Firebase with correct path
        print("Predictions saved locally and to Firebase Storage")
        
        return predictions_df, data
        
    except Exception as e:
        print(f"Error in generate_predictions: {str(e)}")
        raise

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
#        open=predictions_df['Predicted Open'],
#      high=predictions_df['Predicted High'],
#        low=predictions_df['Predicted Low'],
        close=predictions_df['Predicted Close'],
        name='Predicted Price',
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
