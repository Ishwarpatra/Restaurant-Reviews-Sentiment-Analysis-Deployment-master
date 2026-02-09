import os
import pickle
import logging

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

# ---------------------------------------------------------------------------
# Configuration via environment variables
# ---------------------------------------------------------------------------
DEBUG_MODE = os.environ.get("DEBUG", "false").lower() == "true"
ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS", "http://localhost:5173"
).split(",")

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if DEBUG_MODE else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# App initialisation
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Restaurant Review Sentiment Analyser",
    description="ML-powered sentiment analysis for restaurant reviews",
    version="2.0.0",
    debug=DEBUG_MODE,
)

# CORS – use explicit origins; only fall back to wildcard when DEBUG is on
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
# Load model & vectoriser
# ---------------------------------------------------------------------------
model_path = os.path.join(SCRIPT_DIR, "restaurant-sentiment-mnb-model.pkl")
vectorizer_path = os.path.join(SCRIPT_DIR, "cv-transform.pkl")

try:
    classifier = pickle.load(open(model_path, "rb"))
    cv = pickle.load(open(vectorizer_path, "rb"))
    logger.info("Model and vectoriser loaded successfully.")
except FileNotFoundError as exc:
    logger.error("Model files not found: %s", exc)
    raise SystemExit(
        "FATAL: Model pickle files are missing. Run the training script first."
    ) from exc

# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------
class ReviewRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def message_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Review text must not be empty.")
        return v.strip()


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

        vect = cv.transform([message]).toarray()
        prediction = classifier.predict(vect)[0]
        proba = classifier.predict_proba(vect)[0]
        confidence = round(max(proba) * 100, 2)
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
async def predict_api(request: ReviewRequest):
    """JSON API endpoint consumed by the React frontend."""
    try:
        message = request.message
        vect = cv.transform([message]).toarray()
        prediction = int(classifier.predict(vect)[0])
        proba = classifier.predict_proba(vect)[0]
        confidence = round(max(proba) * 100, 2)
        custom_msg = get_witty_response(prediction, message)

        return {
            "prediction": prediction,
            "confidence": confidence,
            "custom_msg": custom_msg,
        }
    except Exception as exc:
        logger.exception("Error in /api/predict")
        return {"error": str(exc), "prediction": None, "confidence": 0}


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health")
async def health():
    return {"status": "healthy", "debug": DEBUG_MODE}


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