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
import torch
import torch.nn as nn
from DataPreprocessing.data_preprocessing import data_augmentation
from firebase_utils import save_df_to_firebase, save_model_to_firebase, file_exists_in_firebase

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

    # Save the cleaned data both locally and to Firebase
    data.to_excel(excel_file_path, index=False)
    save_df_to_firebase(data, 'cleaned_data.csv')
    print(f"Cleaned data saved locally to {excel_file_path} and to Firebase Storage")

else:
    # Try to load from Firebase first, fall back to local if needed
    if file_exists_in_firebase('data/cleaned_data.csv'):
        data = load_df_from_firebase('cleaned_data.csv')
        print("Loaded data from Firebase Storage")
    else:
        data = pd.read_excel(excel_file_path)
        print("Loaded data from local Excel file")
    
    print("Data head")
    print(data.head())
    print("Data info")
    print(data.info())
    print("Data describe")
    print(data.describe())

##data preprocessing
#data=data_augmentation(data)
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
window_size = 60
lstm_input = create_lstm_tensors(features_for_lstm, window_size)

# Input Data (features_for_lstm):
#this is how the lstm tensor is created
# [
#     [f1_t1, f2_t1, f3_t1],  # time step 1
#     [f1_t2, f2_t2, f3_t2],  # time step 2
#     [f1_t3, f2_t3, f3_t3],  # time step 3
#     [f1_t4, f2_t4, f3_t4],  # time step 4
#     [f1_t5, f2_t5, f3_t5]   # time step 5
# ]

# With window_size = 3, the output tensor would look like:
# [
#     # First window
#     [
#         [f1_t1, f2_t1, f3_t1],
#         [f1_t2, f2_t2, f3_t2],
#         [f1_t3, f2_t3, f3_t3]
#     ],
#     # Second window
#     [
#         [f1_t2, f2_t2, f3_t2],
#         [f1_t3, f2_t3, f3_t3],
#         [f1_t4, f2_t4, f3_t4]
#     ],
#     # Third window
#     [
#         [f1_t3, f2_t3, f3_t3],
#         [f1_t4, f2_t4, f3_t4],
#         [f1_t5, f2_t5, f3_t5]
#     ]
# ]


#(n_samples - window_size + 1, window_size, n_features)
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
optimizer = torch.optim.Adam(model.parameters())
criterion = nn.MSELoss()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Convert data to PyTorch tensors
X_train = torch.FloatTensor(X_train).to(device)
y_train = torch.FloatTensor(y_train).to(device)
X_test = torch.FloatTensor(X_test).to(device)
y_test = torch.FloatTensor(y_test).to(device)

# Training loop
epochs = 100
batch_size = 32
history = {'loss': [], 'val_loss': []}  # Initialize history dictionary

for epoch in range(epochs):
    model.train()
    train_losses = []
    for i in range(0, len(X_train), batch_size):
        batch_X = X_train[i:i+batch_size]
        batch_y = y_train[i:i+batch_size]
        
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs.squeeze(), batch_y)
        loss.backward()
        optimizer.step()
        train_losses.append(loss.item())
    
    # Calculate average loss for the epoch
    avg_train_loss = np.mean(train_losses)
    history['loss'].append(avg_train_loss)
    
    # Calculate validation loss
    model.eval()
    with torch.no_grad():
        val_outputs = model(X_test)
        val_loss = criterion(val_outputs.squeeze(), y_test)
        history['val_loss'].append(val_loss.item())

# Save model
torch.save(model.state_dict(), 'Stored_data/lstm_model.pt')
save_model_to_firebase(model, 'lstm_model.pt')
print("Model saved locally and to Firebase Storage")

# After training the model, predict on the test set
predictions = model(X_test).detach().cpu().numpy().flatten()

# Inverse transform both predictions and y_test
predictions = target_scaler.inverse_transform(predictions.reshape(-1, 1)).flatten()
y_test = target_scaler.inverse_transform(y_test.cpu().numpy().reshape(-1, 1)).flatten()

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
save_df_to_firebase(results, 'predictions_test.csv')
print("Predictions saved locally and to Firebase Storage")

# Save preprocessed data to a new Excel file
preprocessed_excel_file_path = 'Stored_data/preprocessed_data.xlsx'
data.to_excel(preprocessed_excel_file_path, index=False)
save_df_to_firebase(data, 'preprocessed_data.csv')
print(f"Preprocessed data saved locally and to Firebase Storage")

# Plotting the training history
plt.figure(figsize=(12, 5))

# Plot loss
plt.subplot(1, 2, 1)
plt.plot(history['loss'], label='Training Loss')
plt.plot(history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend()

# Plot actual vs predicted values instead of MAPE
plt.subplot(1, 2, 2)
plt.scatter(y_test, predictions, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.title('Actual vs Predicted Values')
plt.xlabel('Actual')
plt.ylabel('Predicted')

plt.tight_layout()
plt.show()
