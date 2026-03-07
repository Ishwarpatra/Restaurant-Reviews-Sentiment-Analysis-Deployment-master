import { useState } from 'react';
import axios from 'axios';
import { Mic, Zap, ArrowLeft, BarChart3 } from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || '';

/* ---- SVG Result Icons ---- */
const SmileIcon = () => (
    <svg width="40" height="40" viewBox="0 0 48 48" fill="none">
        <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="2.5" fill="none" />
        <circle cx="17" cy="20" r="2.5" fill="currentColor" />
        <circle cx="31" cy="20" r="2.5" fill="currentColor" />
        <path d="M15 30c2 4 6 6 9 6s7-2 9-6" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" fill="none" />
    </svg>
);

const FrownIcon = () => (
    <svg width="40" height="40" viewBox="0 0 48 48" fill="none">
        <circle cx="24" cy="24" r="20" stroke="currentColor" strokeWidth="2.5" fill="none" />
        <circle cx="17" cy="20" r="2.5" fill="currentColor" />
        <circle cx="31" cy="20" r="2.5" fill="currentColor" />
        <path d="M15 35c2-4 6-6 9-6s7 2 9 6" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" fill="none" />
    </svg>
);

const Analyzer = () => {
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
        <div className="analyzer-page">
            <div className="analyzer-container">
                <div className="glass-card">
                    <div className="glass-card-inner">
                        {/* Card Header */}
                        <div className="card-header-custom">
                            <div className="card-header-icon">
                                {result ? <BarChart3 size={22} /> : <Zap size={22} />}
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
                                            <Mic size={16} />
                                        </button>
                                    </div>

                                    {validationError && (
                                        <div className="validation-msg" id="validation-msg" role="alert">
                                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                                <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
                                            </svg>
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
                                                <Zap size={18} />
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
                                                <BarChart3 size={14} />
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

                                    <div style={{ textAlign: 'center' }}>
                                        <button onClick={resetAnalysis} className="btn-reset" id="analyze-another-button">
                                            <ArrowLeft size={16} />
                                            Analyse Another Review
                                        </button>
                                    </div>
                                </div>
                            )}

                            {/* Error */}
                            {error && (
                                <div className="error-banner" role="alert">
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                                        <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
                                        <line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />
                                    </svg>
                                    {error}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Analyzer;
