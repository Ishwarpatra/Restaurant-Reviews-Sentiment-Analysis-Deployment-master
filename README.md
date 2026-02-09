# Restaurant Review Sentiment Analyser

![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![Licence](https://img.shields.io/badge/Licence-MIT-green)

An **AI-powered web application** that analyses restaurant reviews and predicts whether the sentiment is **positive** or **negative**, complete with confidence scores and witty chef responses.

![App Screenshot](readme_resources/restaurant-review-web-app.gif)

---

## Features

| Feature | Description |
|---|---|
| **Sentiment Analysis** | Multinomial Naive Bayes classifier trained on 1 000 restaurant reviews |
| **Confidence Score** | Probability-based confidence meter for every prediction |
| **Voice Input** | Speak your review using the browser's Speech Recognition API |
| **Modern UI** | Dark glassmorphism design with micro-animations (no Bootstrap) |
| **FastAPI Backend** | High-performance async Python backend |
| **Docker Ready** | Multi-stage Dockerfile for one-command deployment |
| **Security** | Non-root Docker user, env-based config, input validation |

---

## Architecture

```
┌───────────────────────┐     POST /api/predict     ┌──────────────────────┐
│   React Frontend      │ ◄──────────────────────► │   FastAPI Backend     │
│   (Vite + JSX)        │        JSON               │   (Uvicorn)          │
│                       │                           │                      │
│  • Client Validation  │                           │  • TF-IDF Vectoriser │
│  • Voice Input        │                           │  • MNB Classifier    │
│  • Animated Results   │                           │  • Error Handling    │
└───────────────────────┘                           └──────────────────────┘
```

---

## Model Information

### Preprocessing Pipeline
1. **Text Cleaning** – Removal of special characters via regex
2. **Lowercase Conversion** – Normalise case
3. **Tokenisation** – Split into individual words
4. **Stop-word Removal** – NLTK English stop-words
5. **Lemmatisation** – `WordNetLemmatizer` (not Porter Stemmer) for superior linguistic accuracy

### Feature Extraction
- **TF-IDF Vectoriser** (Term Frequency–Inverse Document Frequency)
- Vocabulary size selected automatically via F1-score analysis across candidates `[500, 1000, 1500, 2000, 2500, 3000, ALL]`

### Classification
- **Multinomial Naive Bayes** with α = 0.2
- 80/20 train-test split, `random_state=0`

### Evaluation Metrics
The training script prints a full evaluation report:

| Metric | Description |
|---|---|
| Classification Report | Per-class precision, recall, F1 |
| Confusion Matrix | TP, TN, FP, FN |
| Accuracy | Overall correctness |
| F1-Score (weighted) | Harmonic mean accounting for class imbalance |
| ROC-AUC | Area under the ROC curve |

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- pip

### 1. Clone & Install

```bash
git clone https://github.com/Ishwarpatra/Restaurant-Reviews-Sentiment-Analysis-Deployment.git
cd Restaurant-Reviews-Sentiment-Analysis-Deployment
pip install -r requirements.txt
```

### 2. Train the Model (optional – pre-trained `.pkl` files included)

```bash
python "Restaurant Reviews Sentiment Analyser - Deployment.py"
```

This will:
- Run vocabulary size analysis
- Train the final model with optimal features
- Print full evaluation metrics
- Save `cv-transform.pkl` and `restaurant-sentiment-mnb-model.pkl`

### 3. Build the Frontend

```bash
cd client
npm install
npm run build
cd ..
```

### 4. Run the Server

```bash
python main.py
```

Open **http://localhost:5000** in your browser.

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DEBUG` | `false` | Enable debug mode & CORS wildcard |
| `PORT` | `5000` | Server port |
| `ALLOWED_ORIGINS` | `http://localhost:5173` | Comma-separated CORS origins |

---

## Docker Deployment

```bash
# Build the image
docker build -t restaurant-sentiment .

# Run the container
docker run -p 5000:5000 -e DEBUG=false restaurant-sentiment
```

Works on **any cloud provider** — AWS ECS, Azure Container Instances, GCP Cloud Run, DigitalOcean, etc.

---

## Project Structure

```
├── main.py                        # FastAPI backend (API + static file serving)
├── Restaurant Reviews Sentiment
│   Analyser - Deployment.py       # Training & evaluation script
├── Restaurant_Reviews.tsv         # Dataset (1 000 reviews)
├── restaurant-sentiment-mnb-model.pkl  # Trained classifier
├── cv-transform.pkl               # Fitted TF-IDF vectoriser
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Multi-stage Docker build
├── Procfile                       # Heroku / PaaS entrypoint
├── client/                        # React frontend (Vite)
│   ├── index.html                 # HTML shell with OG tags & favicon
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx                # Main app component
│       ├── index.css              # Design system
│       └── components/
│           ├── Navbar.jsx
│           └── Footer.jsx
└── README.md
```

---

## Security Notes

- **No `debug=True` in production** – Debug mode is toggled via the `DEBUG` env var (defaults to `false`)
- **CORS** – Only allows configured origins in production; wildcard only in debug mode
- **Input Validation** – Server-side via Pydantic validators + client-side JS validation
- **Docker** – Runs as non-root `appuser`
- **Dependencies** – Pinned to latest stable versions

---

## Licence

MIT © Ishwarpatra

---

**Star this repo** if it helped you!
