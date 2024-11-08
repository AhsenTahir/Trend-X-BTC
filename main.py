from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import plotly.graph_objects as go
import torch
import torch.nn as nn
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from data_generator.DataGenerator import Data_Generator
from data_cleaning.data_cleaning import data_cleaning
from DataPreprocessing.data_preprocessing import preprocess_data
from model_architecture.model_architecture import create_lstm_tensors, build_lstm_model
from future_predictions import generate_predictions
import logging
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

# Configure logging
logging.basicConfig(
    filename='btc_prediction.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def train_model():
    try:
        logging.info("Starting model training")
        
        # Generate new data
        Raw_Data = Data_Generator()
        
        # Clean the generated data
        data = data_cleaning(Raw_Data)
        
        # Save the cleaned data
        data.to_excel("Stored_data/cleaned_data.xlsx", index=False)
        
        # Preprocess data
        data, scaler = preprocess_data(data)
        
        # Extract close prices
        close_prices = data['Close'].values
        
        # Remove 'Close' from features
        features_for_lstm = data.drop('Close', axis=1)
        
        # Create LSTM tensors
        window_size = 35
        lstm_input = create_lstm_tensors(features_for_lstm, window_size)
        
        # Prepare target variable
        y = close_prices[window_size-1:]
        
        # Scale target variable
        target_scaler = MinMaxScaler()
        y_scaled = target_scaler.fit_transform(y.reshape(-1, 1)).flatten()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            lstm_input, y_scaled, test_size=0.2, random_state=42
        )
        
        # Build model
        model = build_lstm_model(X_train)
        optimizer = torch.optim.Adam(model.parameters())
        criterion = nn.MSELoss()
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.to(device)
        
        # Convert to PyTorch tensors
        X_train = torch.FloatTensor(X_train).to(device)
        y_train = torch.FloatTensor(y_train).to(device)
        X_test = torch.FloatTensor(X_test).to(device)
        y_test = torch.FloatTensor(y_test).to(device)
        
        # Training loop
        epochs = 50
        batch_size = 32
        
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
        
        # Save model
        torch.save(model.state_dict(), 'Stored_data/lstm_model.pt')
        
        logging.info("Model training completed successfully")
        return True
        
    except Exception as e:
        logging.error(f"Error in model training: {str(e)}")
        return False

@app.get("/")
async def root():
    return {"message": "Bitcoin Price Prediction API"}

@app.post("/update-predictions")
async def update_predictions():
    try:
        # Log the start of update process
        logging.info("Starting prediction update process")
        
        # First train the model with new data
        training_success = await train_model()
        if not training_success:
            raise HTTPException(
                status_code=500,
                detail="Model training failed"
            )
        
        # Generate new predictions
        predictions_df = generate_predictions()
        
        # Save predictions to Excel
        predictions_df.to_excel("Stored_data/predictions.xlsx", index=False)
        
        # Create candlestick chart
        fig = go.Figure()
        
        # Add historical data
        historical_data = pd.read_excel("Stored_data/cleaned_data.xlsx")
        fig.add_trace(go.Candlestick(
            x=historical_data['Date'],
            open=historical_data['Open'],
            high=historical_data['High'],
            low=historical_data['Low'],
            close=historical_data['Close'],
            name='Historical Prices'
        ))
        
        # Add predicted data
        fig.add_trace(go.Candlestick(
            x=predictions_df['Date'],
            open=predictions_df['Predicted Open'],
            high=predictions_df['Predicted High'],
            low=predictions_df['Predicted Low'],
            close=predictions_df['Predicted Close'],
            name='Predicted Prices',
            increasing_line_color='orange',
            decreasing_line_color='red'
        ))
        
        # Update layout
        fig.update_layout(
            title='Bitcoin Price Prediction (Candlestick)',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            xaxis_rangeslider_visible=True,
            xaxis_type='date',
            hovermode="x unified",
            template='plotly_dark'
        )
        
        # Convert the figure to JSON
        chart_json = fig.to_json()
        
        # Log successful update
        logging.info("Prediction update completed successfully")
        
        return JSONResponse(content={
            "message": "Model trained and predictions updated successfully",
            "chart_data": chart_json,
            "last_updated": datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error updating predictions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-predictions")
async def get_predictions():
    try:
        predictions_df = pd.read_excel("Stored_data/predictions.xlsx")
        return JSONResponse(content=predictions_df.to_dict(orient='records'))
    except Exception as e:
        logging.error(f"Error fetching predictions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
