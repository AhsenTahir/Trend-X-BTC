import numpy as np
import pandas as pd
import plotly.graph_objects as go
from tensorflow.keras.models import load_model
from DataPreprocessing.data_preprocessing import preprocess_data
from model_architecture.model_architecture import create_lstm_tensors, build_lstm_model
from sklearn.preprocessing import MinMaxScaler
import torch

# Load historical data with OHLC data
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
print(f"Shape of lstm_input: {lstm_input.shape}")

# Define the number of days for future predictions
x_days = 30  # 30-day future predictions on a daily basis

# Prepare the last window of data for prediction
last_data = lstm_input[-1:, :, :]

# Make predictions for the next x days (daily)
predictions = []
for _ in range(x_days):
    model = build_lstm_model(lstm_input)
    model.load_state_dict(torch.load('Stored_data/lstm_model.pt'))
    model.eval()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    with torch.no_grad():
        last_data = torch.FloatTensor(last_data).to(device)
        predicted_price = model(last_data)
        predicted_price = predicted_price.cpu().numpy()
    predictions.append(predicted_price[0, 0])

    # Move last_data to CPU before numpy operations
    last_data = last_data.cpu().numpy()
    last_data = np.roll(last_data, -1, axis=1)
    last_data[0, -1, :] = predicted_price
    # Convert back to tensor format for next iteration
    last_data = torch.FloatTensor(last_data)

# Create a date range for the future predictions (daily)
last_date = pd.to_datetime(data['Date'].iloc[-1])
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=x_days, freq='D')

# Create a DataFrame for predictions
predictions_df = pd.DataFrame({'Date': future_dates, 'Predicted Close': predictions})

# Inverse transform the predicted prices
predictions_df['Predicted Close'] = close_scaler.inverse_transform(predictions_df[['Predicted Close']])

# For simplicity, we'll assume constant Open, High, Low for predicted values (can be customized)
predictions_df['Predicted Open'] = predictions_df['Predicted Close'] * 0.99  # Example assumption: Open is 1% lower
predictions_df['Predicted High'] = predictions_df['Predicted Close'] * 1.02  # Example assumption: High is 2% higher
predictions_df['Predicted Low'] = predictions_df['Predicted Close'] * 0.98  # Example assumption: Low is 2% lower

# Instead of showing the plot, return the predictions DataFrame
def generate_predictions():
    return predictions_df

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
    increasing_line_color='orange', decreasing_line_color='red'
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