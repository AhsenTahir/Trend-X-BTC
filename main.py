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
data = preprocess_data(data)
print("Data head")
print(data.head())
print("Data info")
print(data.info())
print("Data describe")
print(data.describe())

# Create LSTM tensors
window_size = 35
lstm_input = create_lstm_tensors(data, window_size)
print("LSTM input shape:", lstm_input.shape)  # Check the shape of the LSTM input

# Extract the 'close' feature
close_feature_index = 3  # Adjust this index if 'close' is at a different position
y = lstm_input[:, :, close_feature_index]  # Shape will be (samples, 35)

# Reshape y to match the expected shape for training
y = y[:, -1]  # Use the last time step for y, shape will be (samples,)

# Remove the 'close' feature from lstm_input
lstm_input = np.delete(lstm_input, close_feature_index, axis=2)  # Remove the close feature

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(lstm_input, y, test_size=0.2, random_state=42)

# Build the LSTM model
model = build_lstm_model(X_train)

# Fit the model on the training data and store the training history
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)  # Fit the model with validation

# After training the model, predict on the test set
predictions = model.predict(X_test)  # Use the test set for predictions

# Ensure y_test and predictions are 1-dimensional
y_test = y_test.flatten()  # Reshape y_test if needed
predictions = predictions.flatten()  # Reshape predictions if needed

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
