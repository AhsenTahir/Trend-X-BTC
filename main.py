import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from data_cleaning.data_cleaning import data_cleaning
from data_generator.DataGenerator import Data_Generator
from config import GENERATE_NEW_DATA 
from DataPreprocessing.data_preprocessing import preprocess_data
from model_architecture.model_architecture import create_lstm_tensors, build_lstm_model  
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split  # Import train_test_split
from sklearn.preprocessing import MinMaxScaler  # Add this import

# Define the path to your Excel file
excel_file_path = 'Stored_data/cleaned_data.xlsx'

if GENERATE_NEW_DATA:
    # Generate new data
    Raw_Data = Data_Generator()
    print("Raw Data head")
    print(Raw_Data.head())
    print("Raw Data info")
    print(Raw_Data.info())
    print("Raw Data describe")
    print(Raw_Data.describe())

    # Clean the generated data
    data = data_cleaning(Raw_Data)
    print("Data head")
    print(data.head())
    print("Data info")
    print(data.info())
    print("Data describe")
    print(data.describe())

    # Save the cleaned data to an Excel sheet, overwriting the existing file
    data.to_excel(excel_file_path, index=False)
    print(f"Cleaned data saved to {excel_file_path}")

else:
    # Use the existing data from the Excel file
    data = pd.read_excel(excel_file_path)
    print("Loaded data from existing Excel file")
    print("Data head")
    print(data.head())
    print("Data info")
    print(data.info())
    print("Data describe")
    print(data.describe())

##data preprocessing
data, scaler = preprocess_data(data)  # Modify this function to return the scaler as well
print("Data head")
print(data.head())
print("Data info")
print(data.info())
print("Data describe")
print(data.describe())

# Extract the 'Close' feature before creating LSTM tensors
close_prices = data['Close'].values

# Remove 'Close' from the features used for LSTM input
features_for_lstm = data.drop('Close', axis=1)

# Create LSTM tensors
window_size = 35
lstm_input = create_lstm_tensors(features_for_lstm, window_size)
print("LSTM input shape:", lstm_input.shape)

# Prepare the target variable (y)
y = close_prices[window_size-1:]  # Align with the LSTM input

# Create a separate scaler for the target variable
target_scaler = MinMaxScaler()
y_scaled = target_scaler.fit_transform(y.reshape(-1, 1)).flatten()

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(lstm_input, y_scaled, test_size=0.2, random_state=42)

# Build the LSTM model
model = build_lstm_model(X_train)

# Fit the model on the training data and store the training history
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)  # Fit the model with validation

model.save('Stored_data/lstm_model.h5')

# After training the model, predict on the test set
predictions = model.predict(X_test)  # Use the test set for predictions

# Inverse transform both predictions and y_test
predictions = target_scaler.inverse_transform(predictions.reshape(-1, 1)).flatten()
y_test = target_scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

# Calculate accuracy or error metrics on the test set
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)

# Calculate Mean Absolute Percentage Error (MAPE)
mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100  # MAPE in percentage

print(f'Mean Absolute Error (Test Set): {mae}')
print(f'Mean Squared Error (Test Set): {mse}')
print(f'Mean Absolute Percentage Error (Test Set): {mape:.2f}%')

# Optionally, save predictions to a file for further analysis
results = pd.DataFrame({'Actual': y_test, 'Predicted': predictions})
results.to_excel('Stored_data/predictions_test.xlsx', index=False)

# Save preprocessed data to a new Excel file
preprocessed_excel_file_path = 'Stored_data/preprocessed_data.xlsx'
data.to_excel(preprocessed_excel_file_path, index=False)
print(f"Preprocessed data saved to {preprocessed_excel_file_path}")

# Plotting the training history
plt.figure(figsize=(12, 5))

# Plot loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()

# Plot MAPE
plt.subplot(1, 2, 2)
plt.plot(history.history['mean_absolute_percentage_error'], label='Training MAPE')
plt.title('Mean Absolute Percentage Error (MAPE)')
plt.xlabel('Epochs')
plt.ylabel('MAPE (%)')
plt.legend()

plt.tight_layout()
plt.show()
