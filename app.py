from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel
import numpy as np
import pandas as pd
import datetime
import os
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
from data_cleaning.data_cleaning import data_cleaning
from data_generator.DataGenerator import Data_Generator
from DataPreprocessing.data_preprocessing import preprocess_data
from model_architecture.model_architecture import create_lstm_tensors, build_lstm_model

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI()

# Define the path to the stored model and data
MODEL_PATH = "Stored_data/lstm_model.h5"
EXCEL_FILE_PATH = "Stored_data/cleaned_data.xlsx"
PREPROCESSED_FILE_PATH = "Stored_data/preprocessed_data.xlsx"

# Define input parameters schema using Pydantic
class PredictionRequest(BaseModel):
    symbol: str = "BTCUSDT"  # default symbol is BTCUSDT
    window_size: int = 35
    generate_new_data: bool = False  # Flag to indicate if we need to regenerate data

# Load the trained model
def load_trained_model():
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=500, detail="Trained model not found.")
    model = load_model(MODEL_PATH)
    return model

from datetime import datetime

def prepare_data(symbol, window_size, generate_new_data, model):
    # Step 1: Load or Generate Data
    current_date = datetime.now().strftime("%Y-%m-%d")
    if generate_new_data or not os.path.exists(EXCEL_FILE_PATH):
        data = Data_Generator(start_date=current_date, end_date=current_date)
        data_cleaned = data_cleaning(data)
        data_cleaned.to_excel(EXCEL_FILE_PATH, index=False)
    else:
        data_cleaned = pd.read_excel(EXCEL_FILE_PATH)

    # Step 2: Preprocess the data
    preprocessed_data = preprocess_data(data_cleaned)
    
    # Log the number of features after preprocessing
    logging.info(f"Number of features in preprocessed data: {preprocessed_data.shape[1]}")
    logging.info(f"Columns in preprocessed data: {preprocessed_data.columns.tolist()}")

    preprocessed_data.to_excel(PREPROCESSED_FILE_PATH, index=False)

    # Step 3: Create LSTM tensors
    lstm_input = create_lstm_tensors(preprocessed_data, window_size)

    # Ensure lstm_input has the correct number of time steps (e.g., window_size = 35)
    if lstm_input.shape[1] != window_size:
        raise ValueError(f"Expected window size of {window_size}, but got {lstm_input.shape[1]}.")

    # Use the last window for prediction (ensure feature count matches model input)
    latest_input = lstm_input[-1:, :, :]

    # Dynamically determine the expected feature count based on the model input shape
    expected_feature_count = model.input_shape[-1]

    # Check the feature count
    if latest_input.shape[-1] > expected_feature_count:
        latest_input = latest_input[:, :, :expected_feature_count]
    elif latest_input.shape[-1] < expected_feature_count:
        raise ValueError(f"Expected {expected_feature_count} features, but got {latest_input.shape[2]}.")

    return latest_input


# API Endpoint to get predictions for the current date
@app.post("/predict")
async def get_prediction(request: PredictionRequest):
    try:
        # Step 1: Load the LSTM model
        model = load_trained_model()

        # Step 2: Prepare the data (generate new or use existing)
        lstm_input = prepare_data(request.symbol, request.window_size, request.generate_new_data, model)

        # Step 3: Make predictions using the model
        prediction = model.predict(lstm_input)
        prediction_value = prediction.flatten()[0]  # Get the prediction for the last time step

        # Step 4: Return the result as JSON
        return {
            "symbol": request.symbol,
            "prediction_date": str(datetime.now().date()),
            "predicted_value": float(prediction_value)
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except FileNotFoundError as fnfe:
        raise HTTPException(status_code=404, detail=str(fnfe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example GET endpoint to check server status
@app.get("/")
async def read_root():
    return {"message": "Welcome to the LSTM Prediction API. Use /predict endpoint for predictions."}