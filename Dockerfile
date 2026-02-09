# ─── Stage 1: Build the React Frontend ───────────────────────────────────
FROM node:20-alpine AS build-stage
WORKDIR /app/client
COPY client/package*.json ./
RUN npm ci --production=false
COPY client/ ./
RUN npm run build

# ─── Stage 2: Python Backend ─────────────────────────────────────────────
FROM python:3.11-slim

# Security: create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install Python dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code & model artefacts
COPY main.py .
COPY Restaurant_Reviews.tsv .
COPY restaurant-sentiment-mnb-model.pkl .
COPY cv-transform.pkl .
COPY Procfile .

# Copy the built frontend from Stage 1
COPY --from=build-stage /app/client/dist ./client/dist

# Drop to non-root user
USER appuser

# Expose the port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Default: production mode
ENV DEBUG=false
ENV PORT=5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]