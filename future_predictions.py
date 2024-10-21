import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import load_model
from DataPreprocessing.data_preprocessing import preprocess_data
from model_architecture.model_architecture import create_lstm_tensors
from sklearn.preprocessing import MinMaxScaler

# Load the trained model
MODEL_PATH = "Stored_data/lstm_model.h5"
model = load_model(MODEL_PATH)

# Load historical data
EXCEL_FILE_PATH = "Stored_data/cleaned_data.xlsx"
data = pd.read_excel(EXCEL_FILE_PATH)

# Preprocess the data
preprocessed_data, scaler = preprocess_data(data)

# Print the shape and column names for debugging
print(f"Shape of preprocessed data: {preprocessed_data.shape}")
print(f"Columns: {preprocessed_data.columns}")

# Extract 'Close' prices before removing it from the features
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
x_days = 30

# Prepare the last window of data for prediction
last_data = lstm_input[-1:, :, :]

# Make predictions for the next x days
predictions = []
for _ in range(x_days):
    predicted_price = model.predict(last_data)
    predictions.append(predicted_price[0, 0])

    # Update last_data for the next prediction
    last_data = np.roll(last_data, -1, axis=1)
    last_data[0, -1, :] = predicted_price

# Create a date range for the future predictions
last_date = pd.to_datetime(data['Date'].iloc[-1])
future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=x_days)

# Create a DataFrame for predictions
predictions_df = pd.DataFrame({'Date': future_dates, 'Predicted Price': predictions})

# Inverse transform the predicted prices
predictions_df['Predicted Price'] = close_scaler.inverse_transform(predictions_df[['Predicted Price']])

# Plot the predictions
plt.figure(figsize=(14, 7))
plt.plot(data['Date'], close_prices, label='Historical Prices')
plt.plot(predictions_df['Date'], predictions_df['Predicted Price'], label='Predicted Prices', color='orange')
plt.title('Bitcoin Price Prediction')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
