import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense

def create_lstm_tensors(data, window_size=35):
    """
    Convert the input DataFrame into 3D tensors for LSTM.
    
    Parameters:
    - data: DataFrame containing the features.
    - window_size: The number of time steps to include in each sample.
    
    Returns:
    - X: 3D numpy array of shape (samples, window_size, features)
    """
    # Ensure the data is a numpy array
    data_values = data.values
    
    # Calculate the number of samples
    num_samples = data_values.shape[0] - window_size + 1
    
    # Initialize the tensor
    X = np.zeros((num_samples, window_size, data_values.shape[1]))
    
    # Fill the tensor with sliding windows of data
    for i in range(num_samples):
        X[i] = data_values[i:i + window_size]
    
    return X

def build_lstm_model(lstm_input):
    """
    Build the LSTM model architecture.
    
    Parameters:
    - lstm_input: Input data for the LSTM model.
    
    Returns:
    - model: Compiled Keras Sequential model.
    """
    # Ensure lstm_input is defined before this line
    if lstm_input is None:
        raise ValueError("lstm_input must be provided and cannot be None.")
    
    lstm_input = lstm_input.reshape(lstm_input.shape[0], lstm_input.shape[1], lstm_input.shape[2])  # Ensure it's 3D
    
    model = Sequential()
    
    # LSTM Layer
    model.add(LSTM(units=10, input_shape=lstm_input.shape[1:], activation='tanh', return_sequences=False))
    
    # Dropout Layer
    model.add(Dropout(rate=0.3))
    
    # Dense Layer
    model.add(Dense(units=1, activation='linear'))  # Linear activation for regression
    
    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error', 'mean_absolute_percentage_error'])
    
    return model