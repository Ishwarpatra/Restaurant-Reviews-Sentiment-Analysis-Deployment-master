import { useState } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import './index.css';

// Use relative URL so it works in both dev (via proxy) and production
// In production (Render), frontend & backend share the same origin → use relative URL.
// For local dev, create client/.env with: VITE_API_URL=http://localhost:5000
const API_URL = import.meta.env.VITE_API_URL || '';

function App() {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [validationError, setValidationError] = useState('');

  // ── Client-side validation ────────────────────────────────────────────
  const validate = () => {
    if (!message.trim()) {
      setValidationError('Please enter a restaurant review before submitting.');
      return false;
    }
    if (message.trim().length < 3) {
      setValidationError('Review is too short. Write at least a few words.');
      return false;
    }
    setValidationError('');
    return true;
  };

  // ── Voice Recognition ─────────────────────────────────────────────────
  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setError('Voice input is not supported in this browser.');
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => setIsRecording(true);
    recognition.onend = () => setIsRecording(false);
    recognition.onerror = () => setIsRecording(false);

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setMessage((prev) => (prev ? prev + ' ' : '') + transcript);
      setValidationError('');
    };

    if (isRecording) recognition.stop();
    else recognition.start();
  };

  // ── API Call ──────────────────────────────────────────────────────────
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_URL}/api/predict`, { message: message.trim() });
      if (response.data.error) {
        setError(response.data.error);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError('Failed to connect to the server. Is the backend running?');
    } finally {
      setIsLoading(false);
    }
  };

  // ── Reset ─────────────────────────────────────────────────────────────
  const resetAnalysis = () => {
    setResult(null);
    setMessage('');
    setError('');
    setValidationError('');
  };

  // ── Render ────────────────────────────────────────────────────────────
  return (
    <div className="app-wrapper">
      <Navbar />

      <main className="main-content">
        <div className="glass-card">

          {/* Card Header */}
          <div className="card-header-custom">
            <h2>
              <i className={`fas ${result ? 'fa-chart-bar' : 'fa-comments'}`}></i>
              {result ? 'Analysis Result' : 'Review Analysis'}
            </h2>
            <p className="card-subtitle">
              {result
                ? 'Here\'s what the AI chef thinks about this review'
                : 'Paste a restaurant review and let our AI analyse the sentiment'}
            </p>
          </div>

          <div className="card-body-custom">

            {/* ── INPUT FORM ──────────────────────────────────────── */}
            {!result && (
              <form onSubmit={handleSubmit} noValidate>
                <label className="form-label-custom" htmlFor="review-input">
                  Your Review
                </label>
                <div className="textarea-wrapper">
                  <textarea
                    id="review-input"
                    className={`textarea-custom ${validationError ? 'is-invalid' : ''}`}
                    rows="6"
                    placeholder="e.g. The food was absolutely delicious and the service was outstanding..."
                    value={message}
                    onChange={(e) => {
                      setMessage(e.target.value);
                      if (validationError) setValidationError('');
                    }}
                    maxLength={2000}
                    aria-describedby="validation-msg"
                  />
                  <button
                    type="button"
                    className={`mic-btn ${isRecording ? 'recording' : ''}`}
                    onClick={handleVoiceInput}
                    title={isRecording ? 'Stop recording' : 'Voice input'}
                    aria-label="Toggle voice input"
                  >
                    <i className="fas fa-microphone"></i>
                  </button>
                </div>

                {validationError && (
                  <div className="validation-msg" id="validation-msg" role="alert">
                    <i className="fas fa-exclamation-circle"></i>
                    {validationError}
                  </div>
                )}

                <div className="char-counter">{message.length} / 2000</div>

                <button
                  type="submit"
                  className="btn-submit"
                  disabled={isLoading}
                  id="predict-button"
                >
                  {isLoading ? (
                    <>
                      <span className="spinner"></span>
                      Analysing…
                    </>
                  ) : (
                    <>
                      <i className="fas fa-bolt"></i>
                      Analyse Sentiment
                    </>
                  )}
                </button>
              </form>
            )}

            {/* ── RESULTS ─────────────────────────────────────────── */}
            {result && (
              <div className="result-container">
                <div className={`result-banner ${result.prediction === 1 ? 'positive' : 'negative'}`}>
                  <span className="result-emoji">
                    <i className={`fas ${result.prediction === 1 ? 'fa-face-smile-beam' : 'fa-face-frown'}`}></i>
                  </span>
                  <div className="result-label">
                    {result.prediction === 1 ? 'Positive Review' : 'Negative Review'}
                  </div>
                  <p className="result-msg">{result.custom_msg}</p>
                </div>

                {/* Confidence Meter */}
                <div className="confidence-section">
                  <div className="confidence-label">
                    <span>AI Confidence</span>
                    <span className="confidence-value">{result.confidence}%</span>
                  </div>
                  <div className="progress-track">
                    <div
                      className={`progress-fill ${result.prediction === 1 ? 'positive' : 'negative'}`}
                      style={{ width: `${result.confidence}%` }}
                    />
                  </div>
                </div>

                {/* CTA: Analyse Another */}
                <div style={{ textAlign: 'center' }}>
                  <button onClick={resetAnalysis} className="btn-reset" id="analyze-another-button">
                    <i className="fas fa-arrow-left"></i>
                    Analyse Another Review
                  </button>
                </div>
              </div>
            )}

            {/* Error Banner */}
            {error && (
              <div className="error-banner" role="alert">
                <i className="fas fa-triangle-exclamation"></i>
                {error}
              </div>
            )}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;