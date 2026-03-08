import { useState, useRef } from 'react';
import axios from 'axios';
import { Mic, Zap, ArrowLeft, BarChart3 } from 'lucide-react';

declare global {
    interface Window {
        SpeechRecognition: any;
        webkitSpeechRecognition: any;
    }
}

interface AnalysisResult {
    error?: string;
    prediction: number;
    custom_msg: string;
    confidence: number;
}

const API_URL = (import.meta as any).env.VITE_API_URL || '';
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
    const [message, setMessage] = useState<string>('');
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [isRecording, setIsRecording] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');
    const [validationError, setValidationError] = useState<string>('');
    const recognitionRef = useRef<any>(null);

    const validate = (): boolean => {
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

    const handleVoiceInput = async () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            setError('Voice input is not supported in this browser.');
            return;
        }

        if (isRecording) {
            if (recognitionRef.current) {
                recognitionRef.current.stop();
            }
            setIsRecording(false);
            return;
        }

        // Request microphone permissions explicitly
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            // Stop the media tracks immediately so we don't hold the mic unnecessarily.
            // SpeechRecognition will request its own microphone access.
            stream.getTracks().forEach(track => track.stop());
        } catch (err: any) {
            console.error('Microphone permission denied:', err);
            if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
                setError('Microphone access denied. Please allow microphone permission in your browser settings.');
            } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
                setError('No microphone found. Please connect a microphone to use voice input.');
            } else {
                setError('Error accessing the microphone: ' + err.message);
            }
            return;
        }

        const recognition = new SpeechRecognition();
        recognitionRef.current = recognition;
        recognition.continuous = false;
        recognition.lang = 'en-US';
        recognition.onstart = () => setIsRecording(true);
        recognition.onend = () => setIsRecording(false);
        recognition.onerror = (e: any) => {
            console.error('Speech recognition error', e);
            setIsRecording(false);
        };
        recognition.onresult = (event: any) => {
            const transcript = event.results[0][0].transcript;
            setMessage((prev) => (prev ? prev + ' ' : '') + transcript);
            setValidationError('');
        };

        try {
            recognition.start();
        } catch (e) {
            console.error(e);
            setIsRecording(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
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
                                            rows={5}
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
