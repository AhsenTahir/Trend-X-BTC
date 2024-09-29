import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from data_cleaning.data_cleaning import data_cleaning
from data_generator.DataGenerator import Data_Generator
from config import GENERATE_NEW_DATA 
from DataPreprocessing.data_preprocessing import preprocess_data
from model_architecture.model_architecture import create_lstm_tensors, build_lstm_model  
from sklearn.metrics import mean_absolute_error, mean_squared_error

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
y = lstm_input[:, :, close_feature_index]  # Shape will be (2550, 35)

# Reshape y to match the expected shape for training
y = y[:, -1]  # Use the last time step for y, shape will be (2550,)

# Remove the 'close' feature from lstm_input
lstm_input = np.delete(lstm_input, close_feature_index, axis=2)  # Remove the close feature
model = build_lstm_model(lstm_input)

# Fit the model and store the training history
history = model.fit(lstm_input, y, epochs=50, batch_size=32, validation_split=0.2)  # Fit the model with validation

# After training the model
predictions = model.predict(lstm_input)  # Use the same input shape as during training

# Ensure y and predictions are 1-dimensional
y = y.flatten()  # Add this line to reshape y
predictions = predictions.flatten()  # Add this line to reshape predictions

# Calculate accuracy or error metrics
mae = mean_absolute_error(y, predictions)
mse = mean_squared_error(y, predictions)

# Calculate Mean Absolute Percentage Error (MAPE)
mape = np.mean(np.abs((y - predictions) / y)) * 100  # MAPE in percentage

print(f'Mean Absolute Error: {mae}')
print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Percentage Error: {mape:.2f}%')  # Print MAPE

# Optionally, save predictions to a file for further analysis
print("Shape of y:", y.shape)  # Check the shape of y
print("Shape of predictions:", predictions.shape)  # Check the shape of predictions
# Ensure both are 1-dimensional
if y.ndim != 1 or predictions.ndim != 1:
    raise ValueError("Both y and predictions must be 1-dimensional arrays.")
    
results = pd.DataFrame({'Actual': y, 'Predicted': predictions})
results.to_excel('Stored_data/predictions.xlsx', index=False)

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
plt.title('Model MAPE')
plt.ylabel('MAPE (%)')
plt.xlabel('Epoch')
plt.legend()

plt.tight_layout()
plt.show()