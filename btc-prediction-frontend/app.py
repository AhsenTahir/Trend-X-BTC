import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from keras.models import load_model
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


model = load_model(r'D:\BTC Prediction\BTC-prediction\Stored_data\lstm_model.h5')  # Full path

# Load your results DataFrame (assuming it's saved as a CSV or Excel file)
results_df = pd.read_excel('D:\BTC Prediction\BTC-prediction\Stored_data/predictions_test.xlsx')  # Load the DataFrame with actual and predicted values

@app.route('/')
def home():
    return "Welcome to the BTC Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get the JSON data from the request
    date_str = data.get('date')  # Expecting a date in 'YYYY-MM-DD' format

    # Convert the date string to a datetime object
    date = datetime.strptime(date_str, '%Y-%m-%d')

    # Check if the date exists in the results DataFrame
    if date in results_df['Date'].values:  # Assuming you have a 'Date' column in your DataFrame
        predicted_value = results_df.loc[results_df['Date'] == date, 'Predicted'].values[0]
        return jsonify({'Predicted': predicted_value})  # Return the predicted value
    else:
        return jsonify({'error': 'Date not found in predictions.'}), 404  # Return an error if the date is not found

if __name__ == '__main__':
    app.run(debug=True)