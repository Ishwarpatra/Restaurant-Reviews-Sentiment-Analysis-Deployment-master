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
+-------------------------------+   POST /api/predict   +-----------------------------+
|   React Frontend              | <-------------------> |   FastAPI Backend            |
|   (Vite + JSX)                |        JSON           |   (Uvicorn)                 |
|                               |                       |                             |
|   - Client Validation         |                       |   - TF-IDF Vectoriser       |
|   - Voice Input               |                       |   - MNB Classifier          |
|   - Animated Results          |                       |   - Error Handling          |
+-------------------------------+                       +-----------------------------+
```

---

## Model Information

For full model documentation including architecture rationale, hyperparameter details,
evaluation metrics, limitations, and future improvements, see **[MODEL.md](MODEL.md)**.

### Quick Summary
- **Algorithm**: Multinomial Naive Bayes (alpha=0.2)
- **Features**: TF-IDF Vectoriser with auto-selected vocabulary size
- **Preprocessing**: Text cleaning, contraction expansion, stop-word removal, lemmatisation
- **Metrics**: Accuracy ~77-79%, ROC-AUC ~0.84-0.86

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

### 2. Train the Model (optional -- pre-trained `.pkl` files included)

```bash
python "Restaurant Reviews Sentiment Analyser - Deployment.py"
```

This will:
- Run vocabulary size analysis
- Train the final model with optimal features
- Print full evaluation metrics
- Save `cv-transform.pkl` and `restaurant-sentiment-mnb-model.pkl`

### 2b. Validate the Dataset

```bash
python data_validation.py
```

### 2c. Hyperparameter Tuning (optional)

```bash
python hyperparameter_tuning.py
```

Runs GridSearchCV with cross-validation over alpha and max_features.

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

Works on **any cloud provider** -- AWS ECS, Azure Container Instances, GCP Cloud Run, DigitalOcean, etc.

---

## Testing

```bash
# Install test dependencies (already in requirements.txt)
pip install pytest pytest-asyncio pytest-cov httpx

# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run a specific test file
pytest tests/test_api.py -v
```

---

## Project Structure

```
├── main.py                        # FastAPI backend (API + static file serving)
├── preprocess.py                  # Text preprocessing module
├── data_validation.py             # Dataset quality checks
├── hyperparameter_tuning.py       # GridSearchCV tuning script
├── Restaurant Reviews Sentiment
│   Analyser - Deployment.py       # Training & evaluation script
├── Restaurant_Reviews.tsv         # Dataset (1 000 reviews)
├── restaurant-sentiment-mnb-model.pkl  # Trained classifier
├── cv-transform.pkl               # Fitted TF-IDF vectoriser
├── requirements.txt               # Python dependencies
├── environment.yml                # Conda environment definition
├── Dockerfile                     # Multi-stage Docker build
├── Procfile                       # Heroku / PaaS entrypoint
├── render.yaml                    # Render.com deployment config
├── MODEL.md                       # Model architecture documentation
├── CONTRIBUTING.md                # Contribution guidelines
├── tests/                         # Test suite (pytest)
│   ├── conftest.py                # Shared fixtures
│   ├── test_preprocess.py         # Preprocessing tests
│   ├── test_api.py                # API endpoint tests
│   └── test_data_validation.py    # Data validation tests
├── models/                        # Versioned model artefacts
│   └── README.md                  # Versioning instructions
├── client/                        # React frontend (Vite)
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       └── components/
│           ├── Navbar.jsx
│           └── Footer.jsx
└── README.md
```

---

## Security Notes

- **No `debug=True` in production** -- Debug mode is toggled via the `DEBUG` env var (defaults to `false`)
- **CORS** -- Only allows configured origins in production; wildcard only in debug mode
- **Input Validation** -- Server-side via Pydantic validators + client-side JS validation
- **Docker** -- Runs as non-root `appuser`
- **Dependencies** -- Pinned to latest stable versions

---

## Contributing

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for setup instructions, coding standards,
testing guidelines, and PR process.

---

## Reproducibility

| Method | Command |
|---|---|
| **pip** | `pip install -r requirements.txt` |
| **conda** | `conda env create -f environment.yml` |
| **Docker** | `docker build -t restaurant-sentiment .` |

Model versioning is done via the `models/` directory. See `models/README.md` for conventions.

---

## Licence

MIT (c) Ishwarpatra

---

**Star this repo** if it helped you!
