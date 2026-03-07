# Contributing to Restaurant Review Sentiment Analyser

Thank you for your interest in contributing! This guide will help you get started.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/).
Be respectful, inclusive, and constructive in all interactions.

---

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Git**
- (Optional) **Docker** for containerised development

### Fork & Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/<your-username>/Restaurant-Reviews-Sentiment-Analysis-Deployment.git
cd Restaurant-Reviews-Sentiment-Analysis-Deployment
```

---

## Development Setup

### Backend (Python)

```bash
# Create a virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dev/test dependencies
pip install pytest pytest-cov httpx
```

### Frontend (React + Vite)

```bash
cd client
npm install
cd ..
```

### Running Locally

```bash
# Terminal 1: Backend
python main.py

# Terminal 2: Frontend (dev mode with HMR)
cd client
npm run dev
```

- Backend: http://localhost:5000
- Frontend (dev): http://localhost:5173

### Running with Docker

```bash
docker build -t restaurant-sentiment .
docker run -p 5000:5000 -e DEBUG=true restaurant-sentiment
```

---

## Project Structure

```
.
├── main.py                           # FastAPI backend
├── Restaurant Reviews Sentiment
│   Analyser - Deployment.py          # Training & evaluation script
├── preprocess.py                     # Text preprocessing module
├── data_validation.py                # Data quality checks
├── hyperparameter_tuning.py          # GridSearchCV tuning script
├── Restaurant_Reviews.tsv            # Dataset
├── restaurant-sentiment-mnb-model.pkl
├── cv-transform.pkl
├── requirements.txt
├── environment.yml                   # Conda environment
├── Dockerfile
├── Procfile
├── render.yaml
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_preprocess.py
│   ├── test_api.py
│   └── test_data_validation.py
├── models/                           # Versioned model artefacts
├── client/                           # React frontend
│   └── src/
└── docs/
    └── MODEL.md
```

---

## How to Contribute

### Reporting Bugs

1. Check existing issues first to avoid duplicates
2. Use the bug report template:
   - **Title**: Brief description of the bug
   - **Steps to Reproduce**: Numbered steps to trigger the bug
   - **Expected Behaviour**: What should happen
   - **Actual Behaviour**: What actually happens
   - **Environment**: OS, Python version, browser, etc.

### Suggesting Features

Open an issue with the `enhancement` label. Describe:
- The problem your feature solves
- Proposed solution
- Alternative approaches considered

### Submitting Code

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Write tests** for any new functionality

4. **Run the test suite**:
   ```bash
   pytest --cov=. --cov-report=term-missing
   ```

5. **Submit a pull request**

---

## Coding Standards

### Python

- Follow **PEP 8** style guidelines
- Use **type hints** for function signatures
- Add **docstrings** to all public functions and classes
- Maximum line length: **88 characters** (Black formatter default)
- Use **f-strings** for string formatting
- Use **pathlib** or **os.path** for cross-platform paths

### JavaScript/JSX

- Use **functional components** with hooks (no class components)
- Use **const** over **let** where possible; avoid **var**
- Use **meaningful variable names** (no single-letter names except in loops)
- Components: **PascalCase** filenames (e.g., `Navbar.jsx`)
- Utilities: **camelCase** filenames (e.g., `apiClient.js`)

### Git Commits

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add voice input to review form
fix: handle empty review submission
docs: update MODEL.md with evaluation metrics
test: add API endpoint tests
refactor: extract preprocessing into module
chore: update dependencies
```

---

## Testing

### Running Tests

```bash
# All tests
pytest

# With coverage report
pytest --cov=. --cov-report=term-missing

# Specific test file
pytest tests/test_api.py

# Verbose output
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files `test_<module>.py`
- Name test functions `test_<what_it_tests>`
- Use **fixtures** in `conftest.py` for shared setup
- Aim for **80%+ code coverage**

---

## Pull Request Process

1. **Update documentation** if your change affects user-facing behaviour
2. **Ensure all tests pass** (`pytest`)
3. **Update `requirements.txt`** if you add Python dependencies
4. **Update `package.json`** if you add JavaScript dependencies
5. **Describe your changes** clearly in the PR description
6. **Reference any related issues** using `Closes #123`

### PR Checklist

- [ ] Code follows the project's coding standards
- [ ] Tests added/updated for new functionality
- [ ] Documentation updated (README, MODEL.md, etc.)
- [ ] All tests pass locally
- [ ] No breaking changes (or documented in PR)

---

## Questions?

Open a [Discussion](https://github.com/Ishwarpatra/Restaurant-Reviews-Sentiment-Analysis-Deployment/discussions)
or reach out via the issue tracker.

Thank you for helping improve this project!
