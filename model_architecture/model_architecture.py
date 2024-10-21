import numpy as np
import pandas as pd
from keras.models import Sequential, Model
from keras.layers import LSTM, Dropout, Dense, AdditiveAttention, Permute, Reshape, Multiply, Flatten, Input

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

def build_lstm_model(X_train):
    """
    Build the LSTM model architecture with an attention mechanism.
    
    Parameters:
    - X_train: Input data for the LSTM model.
    
    Returns:
    - model: Compiled Keras Model.
    """
    # Ensure lstm_input is defined before this line
    if X_train is None:
        raise ValueError("X_train must be provided and cannot be None.")
    
    # Define the input layer
    inputs = Input(shape=X_train.shape[1:])
    
    # First LSTM Layer
    lstm_out1 = LSTM(units=70, return_sequences=True)(inputs)
    
    # Second LSTM Layer
    lstm_out2 = LSTM(units=70, return_sequences=True)(lstm_out1)
    
    # Attention Layer
    attention = AdditiveAttention()([lstm_out2, lstm_out2])
    
    # Multiply original output with attention output
    attention_mul = Multiply()([lstm_out2, attention])
    
    # Permute and reshape for attention
    permuted = Permute((2, 1))(attention_mul)
    
    # Dropout Layer
    dropout = Dropout(rate=0.3)(permuted)
    
    # Flatten Layer
    flatten = Flatten()(dropout)
    
    # Dense Layer
    outputs = Dense(units=1, activation='linear')(flatten)
    
    # Create the model
    model = Model(inputs=inputs, outputs=outputs)
    
    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error', 'mean_absolute_percentage_error'])
    
    return model
