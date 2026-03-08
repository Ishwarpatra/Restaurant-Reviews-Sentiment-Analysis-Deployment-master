import { Link } from 'react-router-dom';
import { ArrowRight, Code2, Server, Brain, Container, DatabaseZap, Layers } from 'lucide-react';

const About = () => {
    return (
        <div className="about-page">
            <div className="about-container">
                {/* Hero heading */}
                <div className="about-header">
                    <h1 className="about-title">
                        About <span className="text-gradient">the Model</span>
                    </h1>
                    <p className="about-lead">
                        A look under the hood at the technology, architecture, and design
                        decisions powering the Sentiment Analyser.
                    </p>
                </div>

                {/* Tech stack grid */}
                <div className="about-grid">
                    <div className="about-card">
                        <div className="about-card-icon blue">
                            <Code2 size={24} />
                        </div>
                        <h3>Frontend</h3>
                        <ul className="about-list">
                            <li>React 18 with Vite</li>
                            <li>React Router v6</li>
                            <li>Lucide Icons (SVG)</li>
                            <li>Custom CSS Design System</li>
                            <li>No Bootstrap -- fully custom</li>
                        </ul>
                    </div>

                    <div className="about-card">
                        <div className="about-card-icon emerald">
                            <Server size={24} />
                        </div>
                        <h3>Backend</h3>
                        <ul className="about-list">
                            <li>FastAPI (async)</li>
                            <li>Uvicorn ASGI Server</li>
                            <li>Pydantic Validation</li>
                            <li>Custom Error Handlers</li>
                            <li>CORS &amp; Environment Config</li>
                        </ul>
                    </div>

                    <div className="about-card">
                        <div className="about-card-icon amber">
                            <Brain size={24} />
                        </div>
                        <h3>ML Pipeline</h3>
                        <ul className="about-list">
                            <li>Multinomial Naive Bayes</li>
                            <li>TF-IDF Vectoriser</li>
                            <li>NLTK WordNetLemmatizer</li>
                            <li>GridSearchCV Tuning</li>
                            <li>Cross-Validation (5-fold)</li>
                        </ul>
                    </div>

                    <div className="about-card">
                        <div className="about-card-icon purple">
                            <Container size={24} />
                        </div>
                        <h3>Deployment</h3>
                        <ul className="about-list">
                            <li>Multi-stage Dockerfile</li>
                            <li>Non-root container user</li>
                            <li>Render.com config</li>
                            <li>Health check endpoint</li>
                            <li>Production-ready logging</li>
                        </ul>
                    </div>

                    <div className="about-card">
                        <div className="about-card-icon rose">
                            <DatabaseZap size={24} />
                        </div>
                        <h3>Data</h3>
                        <ul className="about-list">
                            <li>1,000 labelled reviews</li>
                            <li>Binary sentiment (pos/neg)</li>
                            <li>8-check data validation</li>
                            <li>Automated preprocessing</li>
                            <li>Class-balanced dataset</li>
                        </ul>
                    </div>

                    <div className="about-card">
                        <div className="about-card-icon cyan">
                            <Layers size={24} />
                        </div>
                        <h3>Testing</h3>
                        <ul className="about-list">
                            <li>64 pytest tests</li>
                            <li>Async API tests (httpx)</li>
                            <li>Preprocessing unit tests</li>
                            <li>Data validation tests</li>
                            <li>Coverage reporting</li>
                        </ul>
                    </div>
                </div>

                {/* Model details card */}
                <div className="about-model-card">
                    <div className="glass-card-inner">
                        <div className="card-header-custom">
                            <div className="card-header-icon">
                                <Brain size={22} />
                            </div>
                            <h2>Model Architecture</h2>
                            <p className="card-subtitle">
                                Key metrics and design decisions behind the classifier
                            </p>
                        </div>
                        <div className="card-body-custom">
                            <div className="model-stats-grid">
                                <div className="model-stat">
                                    <span className="model-stat-label">Algorithm</span>
                                    <span className="model-stat-value">Multinomial NB</span>
                                </div>
                                <div className="model-stat">
                                    <span className="model-stat-label">Alpha</span>
                                    <span className="model-stat-value">0.2</span>
                                </div>
                                <div className="model-stat">
                                    <span className="model-stat-label">Accuracy</span>
                                    <span className="model-stat-value accent">~77-79%</span>
                                </div>
                                <div className="model-stat">
                                    <span className="model-stat-label">ROC-AUC</span>
                                    <span className="model-stat-value accent">~0.84-0.86</span>
                                </div>
                                <div className="model-stat">
                                    <span className="model-stat-label">Features</span>
                                    <span className="model-stat-value">TF-IDF</span>
                                </div>
                                <div className="model-stat">
                                    <span className="model-stat-label">Dataset</span>
                                    <span className="model-stat-value">1,000 reviews</span>
                                </div>
                            </div>

                            <div style={{ textAlign: 'center', marginTop: '32px' }}>
                                <Link to="/analyze" className="btn-primary-cta" id="about-cta-analyze">
                                    Try It Out
                                    <ArrowRight size={18} />
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default About;
