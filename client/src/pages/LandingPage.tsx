import React from 'react';
import { Link } from 'react-router-dom';
import {
    MessageSquare,
    Zap,
    BarChart3,
    ChevronDown,
    Shield,
    Mic,
    ArrowRight,
} from 'lucide-react';

/* ---- Inline SVG Hero Illustration ---- */
const HeroIllustration = () => (
    <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 480 400"
        width="100%"
        height="auto"
        className="hero-svg"
        aria-hidden="true"
    >
        <defs>
            <linearGradient id="hero-bg" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#F59E0B" stopOpacity="0.08" />
                <stop offset="100%" stopColor="#3B82F6" stopOpacity="0.05" />
            </linearGradient>
            <linearGradient id="hero-accent" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#F59E0B" />
                <stop offset="50%" stopColor="#F97316" />
                <stop offset="100%" stopColor="#EF4444" />
            </linearGradient>
            <linearGradient id="hero-blue" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#3B82F6" />
                <stop offset="100%" stopColor="#8B5CF6" />
            </linearGradient>
        </defs>

        {/* Background circle */}
        <circle cx="240" cy="200" r="170" fill="url(#hero-bg)" />
        <circle
            cx="240"
            cy="200"
            r="170"
            fill="none"
            stroke="url(#hero-accent)"
            strokeWidth="1"
            strokeDasharray="6 8"
            opacity="0.3"
        >
            <animateTransform
                attributeName="transform"
                type="rotate"
                from="0 240 200"
                to="360 240 200"
                dur="60s"
                repeatCount="indefinite"
            />
        </circle>

        {/* Chef hat */}
        <g transform="translate(190, 70)">
            <path
                d="M10 80C4 80 0 68 0 58C0 44 10 34 22 34C24 28 34 22 50 22C66 22 76 28 78 34C90 34 100 44 100 58C100 68 96 80 90 80"
                fill="none"
                stroke="url(#hero-accent)"
                strokeWidth="2.5"
                strokeLinecap="round"
            />
            <rect
                x="10"
                y="80"
                width="80"
                height="10"
                rx="4"
                fill="url(#hero-accent)"
                opacity="0.15"
                stroke="url(#hero-accent)"
                strokeWidth="1.5"
            />
            <line x1="35" y1="90" x2="35" y2="110" stroke="url(#hero-accent)" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="50" y1="90" x2="50" y2="115" stroke="url(#hero-accent)" strokeWidth="1.5" strokeLinecap="round" />
            <line x1="65" y1="90" x2="65" y2="110" stroke="url(#hero-accent)" strokeWidth="1.5" strokeLinecap="round" />
        </g>

        {/* Sentiment face - smile */}
        <g transform="translate(140, 200)">
            <circle cx="100" cy="60" r="55" fill="none" stroke="url(#hero-blue)" strokeWidth="2" />
            <circle cx="80" cy="48" r="6" fill="url(#hero-blue)" />
            <circle cx="120" cy="48" r="6" fill="url(#hero-blue)" />
            <path d="M72 72 Q100 100 128 72" fill="none" stroke="url(#hero-blue)" strokeWidth="3" strokeLinecap="round" />
        </g>

        {/* Review card suggestion */}
        <g transform="translate(290, 240)">
            <rect x="0" y="0" width="140" height="80" rx="12" fill="rgba(22,27,34,0.6)" stroke="rgba(59,130,246,0.2)" strokeWidth="1" />
            <line x1="16" y1="22" x2="90" y2="22" stroke="rgba(201,209,217,0.3)" strokeWidth="2" strokeLinecap="round" />
            <line x1="16" y1="38" x2="110" y2="38" stroke="rgba(201,209,217,0.2)" strokeWidth="2" strokeLinecap="round" />
            <line x1="16" y1="54" x2="70" y2="54" stroke="rgba(201,209,217,0.15)" strokeWidth="2" strokeLinecap="round" />
            <circle cx="120" cy="60" r="10" fill="url(#hero-accent)" opacity="0.3" />
            <path d="M116 60 L120 64 L126 56" stroke="url(#hero-accent)" strokeWidth="2" fill="none" strokeLinecap="round" />
        </g>

        {/* Floating sparkles */}
        <circle cx="120" cy="100" r="3" fill="#FBBF24" opacity="0.5">
            <animate attributeName="opacity" values="0.5;0.1;0.5" dur="3s" repeatCount="indefinite" />
        </circle>
        <circle cx="380" cy="140" r="2.5" fill="#3B82F6" opacity="0.4">
            <animate attributeName="opacity" values="0.4;0.1;0.4" dur="2.5s" repeatCount="indefinite" />
        </circle>
        <circle cx="350" cy="340" r="2" fill="#8B5CF6" opacity="0.4">
            <animate attributeName="opacity" values="0.4;0.1;0.4" dur="4s" repeatCount="indefinite" />
        </circle>
        <circle cx="100" cy="310" r="2.5" fill="#F59E0B" opacity="0.3">
            <animate attributeName="opacity" values="0.3;0.05;0.3" dur="3.5s" repeatCount="indefinite" />
        </circle>
    </svg>
);

const LandingPage = () => {
    return (
        <div className="landing-page">
            {/* ---- Hero Section ---- */}
            <section className="hero-landing">
                <div className="hero-content">
                    <div className="hero-text">
                        <span className="hero-eyebrow">AI-Powered Sentiment Analysis</span>
                        <h1 className="hero-headline">
                            Understand Your Customers'{' '}
                            <span className="text-gradient">True Feelings.</span>
                        </h1>
                        <p className="hero-lead">
                            Instantly analyse restaurant reviews using our ML model. Get
                            confidence scores, reliability metrics, and witty chef responses
                            -- all in real time.
                        </p>
                        <div className="hero-cta-group">
                            <Link to="/analyze" className="btn-primary-cta" id="cta-start-analyzing">
                                Start Analysing
                                <ArrowRight size={18} />
                            </Link>
                            <a href="#features" className="btn-ghost-cta">
                                Learn More
                                <ChevronDown size={16} />
                            </a>
                        </div>
                    </div>
                    <div className="hero-illustration">
                        <HeroIllustration />
                    </div>
                </div>

                {/* Scroll indicator */}
                <a href="#features" className="scroll-indicator" aria-label="Scroll to features">
                    <ChevronDown size={28} />
                </a>
            </section>

            {/* ---- Features Section ---- */}
            <section id="features" className="features-section">
                <div className="features-inner">
                    <h2 className="section-title">Why Use the Sentiment Analyser?</h2>
                    <p className="section-subtitle">
                        Everything you need to decode restaurant reviews at a glance.
                    </p>

                    <div className="features-grid">
                        <div className="feature-card-landing">
                            <div className="feature-icon amber">
                                <Zap size={28} />
                            </div>
                            <h3>Instant Analysis</h3>
                            <p>
                                Paste any review and get positive/negative classification in
                                under a second, powered by a trained Naive Bayes model.
                            </p>
                        </div>

                        <div className="feature-card-landing">
                            <div className="feature-icon blue">
                                <BarChart3 size={28} />
                            </div>
                            <h3>Confidence Metrics</h3>
                            <p>
                                See exactly how confident the AI is with probability-based
                                scoring and a reliability rating for every prediction.
                            </p>
                        </div>

                        <div className="feature-card-landing">
                            <div className="feature-icon purple">
                                <Mic size={28} />
                            </div>
                            <h3>Voice Input</h3>
                            <p>
                                Dictate reviews directly using your browser's native speech
                                recognition API -- no typing required.
                            </p>
                        </div>

                        <div className="feature-card-landing">
                            <div className="feature-icon emerald">
                                <MessageSquare size={28} />
                            </div>
                            <h3>Witty Responses</h3>
                            <p>
                                Every prediction comes with a context-aware, keyword-driven chef
                                response that makes the experience fun.
                            </p>
                        </div>

                        <div className="feature-card-landing">
                            <div className="feature-icon rose">
                                <Shield size={28} />
                            </div>
                            <h3>Input Validation</h3>
                            <p>
                                Robust server-side and client-side validation ensures clean,
                                sanitised input with length and language checks.
                            </p>
                        </div>

                        <div className="feature-card-landing">
                            <div className="feature-icon cyan">
                                <Zap size={28} />
                            </div>
                            <h3>Production Ready</h3>
                            <p>
                                Dockerised, environment-variable-driven, and deployed with
                                health checks. Ready for any cloud platform.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* ---- CTA Banner ---- */}
            <section className="cta-banner">
                <div className="cta-inner">
                    <h2>Ready to analyse your first review?</h2>
                    <p>No sign-up required. Just paste and predict.</p>
                    <Link to="/analyze" className="btn-primary-cta" id="cta-bottom-analyze">
                        Open the Analyser
                        <ArrowRight size={18} />
                    </Link>
                </div>
            </section>
        </div>
    );
};

export default LandingPage;
