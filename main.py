import os
import logging

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, field_validator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# ---------------------------------------------------------------------------
# Configuration via environment variables
# ---------------------------------------------------------------------------
DEBUG_MODE = os.environ.get("DEBUG", "false").lower() == "true"
ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS", "http://localhost:5173"
).split(",")

# ---------------------------------------------------------------------------
# Logging -- structured format for production observability
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------
RATE_LIMIT = os.environ.get("RATE_LIMIT", "10/minute")
limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT])

# ---------------------------------------------------------------------------
# App initialisation
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Restaurant Review Sentiment Analyser",
    description="ML-powered sentiment analysis for restaurant reviews",
    version="2.0.0",
    debug=DEBUG_MODE,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS -- use explicit origins; only fall back to wildcard when DEBUG is on
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if DEBUG_MODE else ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Static files & templates
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

client_assets_dir = os.path.join(SCRIPT_DIR, "client", "dist", "assets")
if os.path.exists(client_assets_dir):
    app.mount("/assets", StaticFiles(directory=client_assets_dir), name="assets")

templates_dir = os.path.join(SCRIPT_DIR, "templates")
if os.path.isdir(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
else:
    templates = None
    logger.warning("No 'templates' directory found – Jinja2 templates disabled.")

# ---------------------------------------------------------------------------
# Load Modern Transformer Model
# ---------------------------------------------------------------------------
try:
    from transformers import pipeline
    logger.info("Loading DistilBERT sentiment analysis pipeline... this may take a moment on boot.")
    
    # device=-1 forces CPU inference to prevent OOM errors on free-tier containers
    sentiment_model = pipeline(
        "sentiment-analysis", 
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
        device=-1 
    )
    logger.info("DistilBERT model loaded successfully into RAM.")
except ImportError as exc:
    logger.error("Transformers library not installed: %s", exc)
    raise SystemExit(
        "FATAL: Missing dependencies. Run `pip install -r requirements.txt`"
    ) from exc
except Exception as exc:
    logger.error("Failed to load model: %s", exc)
    raise SystemExit(
        "FATAL: Could not initialise the transformer pipeline."
    ) from exc

# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------
MAX_REVIEW_LENGTH = 5000


class ReviewRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def message_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Review text must not be empty.")
        stripped = v.strip()
        if len(stripped) > MAX_REVIEW_LENGTH:
            raise ValueError(
                f"Review text must not exceed {MAX_REVIEW_LENGTH} characters."
            )
        return stripped


# ---------------------------------------------------------------------------
# Helper: witty chef response
# ---------------------------------------------------------------------------
def get_witty_response(prediction: int, text: str) -> str:
    lower = text.lower()
    if prediction == 0:
        if any(w in lower for w in ["wait", "slow", "time", "hour"]):
            return "Yikes! Our snails move faster than that service. Message received!"
        if any(w in lower for w in ["taste", "flavor", "salty", "bland", "cold"]):
            return "Did the chef fall asleep? We're sending this feedback to the kitchen!"
        if "money" in lower or "expensive" in lower:
            return "Ouch, that hurts the wallet and the feelings."
        return "We messed up. Thanks for the honest reality check."
    else:
        if any(w in lower for w in ["delicious", "yummy", "tasty", "great food"]):
            return "Chef's Kiss! We're framing this review!"
        if any(w in lower for w in ["staff", "service", "waiter", "waitress"]):
            return "Give that staff member a raise!"
        if "atmosphere" in lower or "place" in lower:
            return "Vibes: Immaculate."
        return "You just made our day!"


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return a friendly JSON error for Pydantic validation failures."""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error.get("loc", []))
        errors.append({"field": field, "message": error.get("msg", "")})
    return JSONResponse(
        status_code=422,
        content={"error": "Validation failed", "details": errors},
    )


@app.exception_handler(400)
async def bad_request_handler(request: Request, exc):
    return JSONResponse(
        status_code=400,
        content={"error": "Bad request", "detail": str(exc.detail) if hasattr(exc, 'detail') else "Invalid request."},
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "detail": "The requested resource does not exist."},
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    logger.exception("Internal server error")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "An unexpected error occurred."},
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
async def read_index():
    index_path = os.path.join(SCRIPT_DIR, "client", "dist", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"detail": "Frontend not built. Run `npm run build` in /client first."}


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, message: str = Form(...)):
    """Legacy form-based predict route (Jinja2 template)."""
    if templates is None:
        return HTMLResponse("<h1>Templates directory missing</h1>", status_code=500)
    try:
        if not message.strip():
            return templates.TemplateResponse(
                "result.html",
                {"request": request, "prediction": None, "error": "Please enter a valid review."},
            )

        result = sentiment_model(message)[0]
        prediction = 1 if result["label"] == "POSITIVE" else 0
        confidence = round(result["score"] * 100, 2)
        custom_msg = get_witty_response(prediction, message)

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "prediction": prediction,
                "confidence": confidence,
                "custom_msg": custom_msg,
            },
        )
    except Exception as exc:
        logger.exception("Error during prediction")
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "prediction": None, "error": f"An error occurred: {exc}"},
        )


@app.post("/api/predict")
@limiter.limit(RATE_LIMIT)
async def predict_api(request: Request, body: ReviewRequest):
    """JSON API endpoint consumed by the React frontend."""
    try:
        message = body.message
        logger.info("Prediction request | length=%d | preview='%s'",
                    len(message), message[:80])

        # Reject non-ASCII-heavy input (likely non-English)
        ascii_ratio = sum(1 for c in message if ord(c) < 128) / max(len(message), 1)
        if ascii_ratio < 0.5:
            logger.warning("Non-English input rejected | ascii_ratio=%.2f", ascii_ratio)
            raise HTTPException(
                status_code=400,
                detail="Input appears to be non-English. This model only supports English reviews.",
            )

        # Modern Inference
        result = sentiment_model(message[:512])[0]  # truncate to DistilBERT max context
        prediction = 1 if result["label"] == "POSITIVE" else 0
        confidence = round(result["score"] * 100, 2)
        custom_msg = get_witty_response(prediction, message)

        logger.info("Prediction result | sentiment=%s | confidence=%.2f%%",
                    "positive" if prediction == 1 else "negative", confidence)

        return {
            "prediction": prediction,
            "confidence": confidence,
            "custom_msg": custom_msg,
        }
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as exc:
        logger.exception("Error in /api/predict")
        raise HTTPException(
            status_code=500,
            detail="An error occurred during prediction. Please try again.",
        ) from exc


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health")
async def health():
    return {"status": "healthy", "debug": DEBUG_MODE}

@app.get("/api/health")
async def health_check():
    return {"status": "awake", "chef": "ready"}


# ---------------------------------------------------------------------------
# SPA catch-all -- serves index.html for client-side routes
# (must be registered LAST so it does not shadow API routes)
# ---------------------------------------------------------------------------
@app.get("/{full_path:path}")
async def spa_catch_all(full_path: str):
    """Serve the React SPA for any route not matched above."""
    index_path = os.path.join(SCRIPT_DIR, "client", "dist", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(
        status_code=404,
        content={"detail": "Frontend not built. Run `npm run build` in /client first."},
    )


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=DEBUG_MODE,
    )