import { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css'; // Your original styles

function App() {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [error, setError] = useState('');

  // Voice Recognition Setup
  const handleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert("Voice input not supported in this browser.");
      return;
    }
    
    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => setIsRecording(true);
    recognition.onend = () => setIsRecording(false);
    
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setMessage((prev) => prev + " " + transcript);
    };

    if (isRecording) recognition.stop();
    else recognition.start();
  };

  // API Call
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return alert("Please enter a review.");

    try {
      // Point this to your FastAPI backend URL
      const response = await axios.post('http://localhost:5000/api/predict', { message });
      setResult(response.data);
      setError('');
    } catch (err) {
      setError("Failed to connect to the chef. Is the backend running?");
    }
  };

  const resetAnalysis = () => {
    setResult(null);
    setMessage('');
  };

  return (
    <div className="d-flex flex-column min-vh-100">
      <Navbar />
      
      <div className="container flex-grow-1 py-5">
        <div className="row justify-content-center">
          <div className="col-md-8">
            <div className="card shadow">
              <div className="card-header bg-primary text-white">
                <h2 className="mb-0">
                  <i className={`fas ${result ? 'fa-chart-bar' : 'fa-comments'} me-2`}></i>
                  {result ? 'Analysis Result' : 'Review Analysis'}
                </h2>
              </div>
              
              <div className="card-body text-center">
                
                {/* VIEW 1: INPUT FORM */}
                {!result && (
                  <>
                    <p className="card-text text-muted">A React + FastAPI Web App.</p>
                    <form onSubmit={handleSubmit}>
                      <div className="mb-3 position-relative">
                        <label className="form-label fw-bold">Enter Your Review:</label>
                        <textarea 
                          className="form-control" 
                          rows="8" 
                          placeholder="Type here or click the mic..." 
                          value={message}
                          onChange={(e) => setMessage(e.target.value)}
                          required 
                        />
                        <button 
                          type="button" 
                          className={`btn position-absolute bottom-0 end-0 m-3 rounded-circle ${isRecording ? 'btn-danger' : 'btn-secondary'}`}
                          onClick={handleVoiceInput}
                        >
                          <i className="fas fa-microphone"></i>
                        </button>
                      </div>
                      <button type="submit" className="btn btn-primary w-100">
                        <i className="fas fa-search me-2"></i>Predict Sentiment
                      </button>
                    </form>
                  </>
                )}

                {/* VIEW 2: RESULTS DISPLAY */}
                {result && (
                  <div className="results-container">
                    <div className={`alert ${result.prediction === 1 ? 'alert-success' : 'alert-danger'} shadow-sm`}>
                      <h1 className="display-4">
                        <i className={`fas ${result.prediction === 1 ? 'fa-laugh-beam' : 'fa-frown-open'}`}></i>
                        {result.prediction === 1 ? ' Positive' : ' Negative'}
                      </h1>
                      <p className="lead">{result.custom_msg}</p>
                    </div>

                    {/* Confidence Meter */}
                    <div className="card mt-4 mx-auto" style={{maxWidth: '500px'}}>
                      <div className="card-body">
                        <h5 className="card-title text-muted">AI Confidence Score</h5>
                        <div className="progress" style={{height: '25px'}}>
                          <div 
                            className={`progress-bar progress-bar-striped progress-bar-animated ${result.prediction === 1 ? 'bg-success' : 'bg-danger'}`} 
                            style={{width: `${result.confidence}%`}}
                          >
                            {result.confidence}%
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="mt-4">
                      <button onClick={resetAnalysis} className="btn btn-outline-primary btn-lg">
                        <i className="fas fa-redo me-2"></i>Analyze Another
                      </button>
                    </div>
                  </div>
                )}

                {error && <div className="alert alert-warning mt-3">{error}</div>}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <Footer />
    </div>
  );
}

export default App;