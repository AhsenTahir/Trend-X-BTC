import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Ensure you have some basic styles

function App() {
  const [date, setDate] = useState('2024-06-30'); // Default date to 30th June 2024
  const [prediction, setPrediction] = useState(null); // Store prediction result
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error state

  const handleChange = (e) => {
    setDate(e.target.value); // Update date state
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null); // Reset error state
    try {
      const response = await axios.post('http://localhost:5000/predict', { date });
      setPrediction(response.data.prediction); // Set prediction result
    } catch (error) {
      console.error('Error making prediction:', error);
      setError('Failed to fetch prediction. Please try again.'); // Set error message
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>BTC Price Prediction</h1>
        <p>Get the predicted closing value for Bitcoin on a specific date.</p>
      </header>
      <form onSubmit={handlePredict} className="prediction-form">
        <label htmlFor="date">Select Date:</label>
        <input
          type="date"
          id="date"
          value={date}
          onChange={handleChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Predict'}
        </button>
      </form>
      {error && <div className="error">{error}</div>}
      {prediction !== null && (
        <div className="result">
          <h2>Predicted Closing Value for {date}:</h2>
          <h3>${prediction.toFixed(2)}</h3>
        </div>
      )}
    </div>
  );
}

export default App;