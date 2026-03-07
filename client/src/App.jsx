import { useState } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import './index.css';

const API_URL = import.meta.env.VITE_API_URL || '';

/* ── SVG Icon Components ───────────────────────────────────────────────── */

const ChefHatIcon = ({ size = 80 }) => (
  <svg width={size} height={size} viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="hat-grad" x1="10" y1="10" x2="70" y2="70" gradientUnits="userSpaceOnUse">
        <stop offset="0%" stopColor="#F59E0B"/>
        <stop offset="50%" stopColor="#F97316"/>
        <stop offset="100%" stopColor="#EF4444"/>
      </linearGradient>
      <linearGradient id="sparkle-grad" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="#FBBF24"/>
        <stop offset="100%" stopColor="#F59E0B"/>
      </linearGradient>
    </defs>
    {/* Chef hat body */}
    <path d="M20 42C14 42 10 36 10 30C10 22 16 16 24 16C26 12 32 8 40 8C48 8 54 12 56 16C64 16 70 22 70 30C70 36 66 42 60 42" stroke="url(#hat-grad)" strokeWidth="2.5" fill="none" strokeLinecap="round"/>
    {/* Hat band */}
    <rect x="20" y="42" width="40" height="8" rx="3" fill="url(#hat-grad)" opacity="0.2" stroke="url(#hat-grad)" strokeWidth="1.5"/>
    {/* Hat pleats */}
    <line x1="30" y1="50" x2="30" y2="62" stroke="url(#hat-grad)" strokeWidth="1.5" strokeLinecap="round"/>
    <line x1="40" y1="50" x2="40" y2="65" stroke="url(#hat-grad)" strokeWidth="1.5" strokeLinecap="round"/>
    <line x1="50" y1="50" x2="50" y2="62" stroke="url(#hat-grad)" strokeWidth="1.5" strokeLinecap="round"/>
    {/* Bottom */}
    <path d="M22 62C22 62 28 68 40 68C52 68 58 62 58 62" stroke="url(#hat-grad)" strokeWidth="2" strokeLinecap="round" fill="none"/>
    {/* Sparkles */}
    <circle cx="12" cy="12" r="2" fill="url(#sparkle-grad)" opacity="0.7">
      <animate attributeName="opacity" values="0.7;0.2;0.7" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="68" cy="10" r="1.5" fill="url(#sparkle-grad)" opacity="0.5">
      <animate attributeName="opacity" values="0.5;0.1;0.5" dur="2.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="72" cy="50" r="1.8" fill="url(#sparkle-grad)" opacity="0.6">
      <animate attributeName="opacity" values="0.6;0.15;0.6" dur="3s" repeatCount="indefinite"/>
    </circle>
    {/* Star sparkle */}
    <path d="M8 48L9.5 44L11 48L15 49.5L11 51L9.5 55L8 51L4 49.5Z" fill="#FBBF24" opacity="0.4">
      <animate attributeName="opacity" values="0.4;0.1;0.4" dur="2.8s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="rotate" from="0 9.5 49.5" to="360 9.5 49.5" dur="8s" repeatCount="indefinite"/>
    </path>
  </svg>
);

const AnalyseIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
  </svg>
);

const ArrowLeftIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M19 12H5M12 19l-7-7 7-7"/>
  </svg>
);

const MicIcon = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"/>
    <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
    <line x1="12" y1="19" x2="12" y2="22"/>
  </svg>
);

const SmileIcon = () => (
  <svg width="36" height="36" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="2.5" fill="none"/>
    <circle cx="17" cy="20" r="2.5" fill="currentColor"/>
    <circle cx="31" cy="20" r="2.5" fill="currentColor"/>
    <path d="M15 30c2 4 6 6 9 6s7-2 9-6" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" fill="none"/>
    {/* Sparkle eyes */}
    <circle cx="17" cy="19" r="0.8" fill="white" opacity="0.6"/>
    <circle cx="31" cy="19" r="0.8" fill="white" opacity="0.6"/>
  </svg>
);

const FrownIcon = () => (
  <svg width="36" height="36" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="2.5" fill="none"/>
    <circle cx="17" cy="20" r="2.5" fill="currentColor"/>
    <circle cx="31" cy="20" r="2.5" fill="currentColor"/>
    <path d="M15 35c2-4 6-6 9-6s7 2 9 6" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" fill="none"/>
  </svg>
);

const AlertIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
    <line x1="12" y1="9" x2="12" y2="13"/>
    <line x1="12" y1="17" x2="12.01" y2="17"/>
  </svg>
);

const ValidationIcon = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10"/>
    <line x1="12" y1="8" x2="12" y2="12"/>
    <line x1="12" y1="16" x2="12.01" y2="16"/>
  </svg>
);

const BarChartIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="20" x2="18" y2="10"/>
    <line x1="12" y1="20" x2="12" y2="4"/>
    <line x1="6" y1="20" x2="6" y2="14"/>
  </svg>
);

const ChatIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
  </svg>
);

const GaugeIcon = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2a10 10 0 100 20 10 10 0 000-20z"/>
    <path d="M12 6v6l4 2"/>
  </svg>
);

/* Feature pill icons */
const SparklesSvg = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5z"/>
  </svg>
);

const ShieldSvg = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
  </svg>
);

const VoiceSvg = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8B5CF6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2a3 3 0 00-3 3v7a3 3 0 006 0V5a3 3 0 00-3-3z"/>
    <path d="M19 10v2a7 7 0 01-14 0v-2"/>
  </svg>
);


function App() {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [validationError, setValidationError] = useState('');

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

  const resetAnalysis = () => {
    setResult(null);
    setMessage('');
    setError('');
    setValidationError('');
  };

  return (
    <div className="app-wrapper">
      {/* Background Effects */}
      <div className="bg-effects">
        <div className="bg-gradient-1" />
        <div className="bg-gradient-2" />
        <div className="bg-gradient-3" />
        <div className="bg-grid" />
      </div>

      <Navbar />

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-icon">
          <ChefHatIcon size={80} />
        </div>
        <h1 className="hero-title">
          <span className="text-gradient">Restaurant Review</span>
          <br />
          Sentiment Analyser
        </h1>
        <p className="hero-description">
          Paste any restaurant review and our AI will instantly determine the sentiment
          with a confidence score and a witty chef response.
        </p>
        <div className="hero-features">
          <span className="feature-pill">
            <SparklesSvg />
            AI-Powered NLP
          </span>
          <span className="feature-pill">
            <ShieldSvg />
            Confidence Score
          </span>
          <span className="feature-pill">
            <VoiceSvg />
            Voice Input
          </span>
        </div>
      </section>

      <main className="main-content">
        <div className="glass-card">
          <div className="glass-card-inner">

            {/* Card Header */}
            <div className="card-header-custom">
              <div className="card-header-icon">
                {result ? <BarChartIcon /> : <ChatIcon />}
              </div>
              <h2>{result ? 'Analysis Result' : 'Review Analysis'}</h2>
              <p className="card-subtitle">
                {result
                  ? "Here's what the AI chef thinks about this review"
                  : 'Type or speak your review below to get instant sentiment analysis'}
              </p>
            </div>

            <div className="card-body-custom">

              {/* INPUT FORM */}
              {!result && (
                <form onSubmit={handleSubmit} noValidate>
                  <label className="form-label-custom" htmlFor="review-input">
                    Your Review
                    <span className="label-hint">English only</span>
                  </label>
                  <div className="textarea-wrapper">
                    <textarea
                      id="review-input"
                      className={`textarea-custom ${validationError ? 'is-invalid' : ''}`}
                      rows="5"
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
                      <MicIcon />
                    </button>
                  </div>

                  {validationError && (
                    <div className="validation-msg" id="validation-msg" role="alert">
                      <ValidationIcon />
                      {validationError}
                    </div>
                  )}

                  <div className="char-counter">{message.length} / 2,000</div>

                  <button
                    type="submit"
                    className="btn-submit"
                    disabled={isLoading}
                    id="predict-button"
                  >
                    {isLoading ? (
                      <>
                        <span className="spinner" />
                        Analysing...
                      </>
                    ) : (
                      <>
                        Analyse Sentiment
                        <AnalyseIcon />
                      </>
                    )}
                  </button>
                </form>
              )}

              {/* RESULTS */}
              {result && (
                <div className="result-container">
                  <div className={`result-banner ${result.prediction === 1 ? 'positive' : 'negative'}`}>
                    <div className="result-icon-wrapper">
                      {result.prediction === 1 ? <SmileIcon /> : <FrownIcon />}
                    </div>
                    <div className="result-label">
                      {result.prediction === 1 ? 'Positive Review' : 'Negative Review'}
                    </div>
                    <p className="result-msg">"{result.custom_msg}"</p>
                  </div>

                  {/* Confidence Meter */}
                  <div className="confidence-section">
                    <div className="confidence-label">
                      <span className="confidence-label-text">
                        <GaugeIcon />
                        AI Confidence
                      </span>
                      <span className="confidence-value">{result.confidence}%</span>
                    </div>
                    <div className="progress-track">
                      <div
                        className={`progress-fill ${result.prediction === 1 ? 'positive' : 'negative'}`}
                        style={{ width: `${result.confidence}%` }}
                      />
                    </div>

                    {/* Stats */}
                    <div className="result-stats">
                      <div className="stat-card">
                        <div className="stat-card-label">Sentiment</div>
                        <div className={`stat-card-value ${result.prediction === 1 ? 'positive' : 'negative'}`}>
                          {result.prediction === 1 ? 'Positive' : 'Negative'}
                        </div>
                      </div>
                      <div className="stat-card">
                        <div className="stat-card-label">Reliability</div>
                        <div className={`stat-card-value ${result.confidence >= 70 ? 'positive' : 'negative'}`}>
                          {result.confidence >= 85 ? 'Very High' : result.confidence >= 70 ? 'High' : result.confidence >= 55 ? 'Moderate' : 'Low'}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* CTA */}
                  <div style={{ textAlign: 'center' }}>
                    <button onClick={resetAnalysis} className="btn-reset" id="analyze-another-button">
                      <ArrowLeftIcon />
                      Analyse Another Review
                    </button>
                  </div>
                </div>
              )}

              {/* Error Banner */}
              {error && (
                <div className="error-banner" role="alert">
                  <AlertIcon />
                  {error}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;