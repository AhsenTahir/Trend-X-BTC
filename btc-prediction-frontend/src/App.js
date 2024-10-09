import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import CircularProgress from '@material-ui/core/CircularProgress';

function App() {
  const [message, setMessage] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dataGenerated, setDataGenerated] = useState(false);

  const generateDataForToday = async () => {
    setLoading(true);
    setMessage('');
    setPrediction(null);
    try {
      const response = await axios.post('http://localhost:8080/generate_data_for_today');
      setMessage(response.data.message);
      setDataGenerated(true);
    } catch (error) {
      setMessage(error.response ? error.response.data.detail : 'An error occurred while generating data.');
    } finally {
      setLoading(false);
    }
  };

  const predictForToday = async () => {
    if (!dataGenerated) {
      setMessage('Please generate data for today first.');
      return;
    }
    setLoading(true);
    setMessage('');
    try {
      const response = await axios.post('http://localhost:8080/predict_for_today');
      setPrediction(response.data.predicted_value);
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response ? error.response.data.detail : 'An error occurred while making the prediction.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Predict Today's Data</h1>
        <div className="button-group">
          <button onClick={generateDataForToday} disabled={loading}>
            {loading ? <CircularProgress size={20} /> : 'Generate Data for Today'}
          </button>
          <button onClick={predictForToday} disabled={loading || !dataGenerated}>
            {loading ? <CircularProgress size={20} /> : 'Predict for Today'}
          </button>
        </div>
        {message && <p className="message">{message}</p>}
        {prediction !== null && <p className="prediction">Predicted Value for Today: {prediction}</p>}
      </header>
    </div>
  );
}

export default App;