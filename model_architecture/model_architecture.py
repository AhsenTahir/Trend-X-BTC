import torch
import torch.nn as nn
import numpy as np
import pandas as pd

def create_lstm_tensors(data, window_size=35):
    """Convert the input DataFrame into tensors for LSTM."""
    data_values = data.values
    num_samples = data_values.shape[0] - window_size + 1
    X = np.zeros((num_samples, window_size, data_values.shape[1]))
    
    for i in range(num_samples):
        X[i] = data_values[i:i + window_size]
    
    return torch.FloatTensor(X)

class LSTMAttention(nn.Module):
    def __init__(self, input_dim, window_size, hidden_dim=64):
        super(LSTMAttention, self).__init__()
        self.window_size = window_size
        self.lstm1 = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.lstm2 = nn.LSTM(hidden_dim, hidden_dim, batch_first=True)
        self.attention = nn.MultiheadAttention(hidden_dim, num_heads=4, batch_first=True)
        self.dropout = nn.Dropout(0.3)
        self.flatten = nn.Flatten()
        self.fc = nn.Linear(hidden_dim * window_size, 1)
    
    def forward(self, x):
        lstm_out1, _ = self.lstm1(x)
        lstm_out2, _ = self.lstm2(lstm_out1)
        attention_out, _ = self.attention(lstm_out2, lstm_out2, lstm_out2)
        attention_mul = lstm_out2 * attention_out
        dropout_out = self.dropout(attention_mul)
        flattened = self.flatten(dropout_out)
        output = self.fc(flattened)
        return output

def build_lstm_model(X_train):
    """Build the LSTM model with attention mechanism."""
    if X_train is None:
        raise ValueError("X_train must be provided")
    
    input_dim = X_train.shape[2]
    window_size = X_train.shape[1]
    model = LSTMAttention(input_dim, window_size)
    return model
