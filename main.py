from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import os
import uvicorn

app = FastAPI()

# Enable CORS so your React app (port 5173) can talk to FastAPI (port 5000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Mount the React build's 'assets' folder
# Note: We check if the directory exists to avoid crashing in dev mode
if os.path.exists("client/dist/assets"):
    app.mount("/assets", StaticFiles(directory="client/dist/assets"), name="assets")

# 2. Setup Templates (Jinja2) - kept for fallback
templates = Jinja2Templates(directory="templates")

# 3. Load Model & Vectorizer (Same logic as before)
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'restaurant-sentiment-mnb-model.pkl')
vectorizer_path = os.path.join(script_dir, 'cv-transform.pkl')

classifier = pickle.load(open(model_path, 'rb'))
cv = pickle.load(open(vectorizer_path,'rb'))

# NEW: Create a data model for the request
class ReviewRequest(BaseModel):
    message: str

# 4. Serve the React Entry Point for the Root
@app.get("/")
async def read_index():
    return FileResponse('client/dist/index.html')

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, message: str = Form(...)):
    try:
        if not message.strip():
            return templates.TemplateResponse("result.html", {
                "request": request, 
                "prediction": None, 
                "error": "Please enter a valid review."
            })
        
        # Prediction Logic (Identical to Flask)
        data = [message]
        vect = cv.transform(data).toarray()
        prediction = classifier.predict(vect)[0]
        proba = classifier.predict_proba(vect)[0]
        confidence = round(max(proba) * 100, 2)

        # "The Witty Chef" Logic (Identical copy-paste)
        custom_msg = ""
        lower_msg = message.lower()
        
        if prediction == 0: # Negative Review
            if any(x in lower_msg for x in ["wait", "slow", "time", "hour"]):
                custom_msg = "Yikes! 🐌 Our snails move faster than that service. Message received!"
            elif any(x in lower_msg for x in ["taste", "flavor", "salty", "bland", "cold"]):
                custom_msg = "Did the chef fall asleep? 🧂 We're sending this feedback to the kitchen!"
            elif "money" in lower_msg or "expensive" in lower_msg:
                custom_msg = "Ouch, that hurts the wallet and the feelings. 💸"
            else:
                custom_msg = "We messed up. Thanks for the honest reality check."
        else: # Positive Review
            if any(x in lower_msg for x in ["delicious", "yummy", "tasty", "great food"]):
                custom_msg = "Chef's Kiss! 👩‍🍳💋 We're framing this review!"
            elif any(x in lower_msg for x in ["staff", "service", "waiter", "waitress"]):
                custom_msg = "Give that staff member a raise! 🏆"
            elif "atmosphere" in lower_msg or "place" in lower_msg:
                custom_msg = "Vibes: Immaculate. ✨"
            else:
                custom_msg = "You just made our day! 😊"

        return templates.TemplateResponse("result.html", {
            "request": request,
            "prediction": prediction,
            "confidence": confidence,
            "custom_msg": custom_msg
        })

    except Exception as e:
        return templates.TemplateResponse("result.html", {
            "request": request, 
            "prediction": None, 
            "error": f"An error occurred: {str(e)}"
        })

# NEW: Create a data API endpoint for React
@app.post("/api/predict")
async def predict_api(request: ReviewRequest):
    message = request.message
    
    # 1. Prediction Logic (Same as before)
    data = [message]
    vect = cv.transform(data).toarray()
    prediction = int(classifier.predict(vect)[0]) # Convert to standard int
    proba = classifier.predict_proba(vect)[0]
    confidence = round(max(proba) * 100, 2)

    # 2. Witty Chef Logic (Same as before)
    custom_msg = ""
    lower_msg = message.lower()
    if prediction == 0: # Negative Review
        if any(x in lower_msg for x in ["wait", "slow", "time", "hour"]):
            custom_msg = "Yikes! 🐌 Our snails move faster than that service. Message received!"
        elif any(x in lower_msg for x in ["taste", "flavor", "salty", "bland", "cold"]):
            custom_msg = "Did the chef fall asleep? 🧂 We're sending this feedback to the kitchen!"
        elif "money" in lower_msg or "expensive" in lower_msg:
            custom_msg = "Ouch, that hurts the wallet and the feelings. 💸"
        else:
            custom_msg = "We messed up. Thanks for the honest reality check."
    else: # Positive Review
        if any(x in lower_msg for x in ["delicious", "yummy", "tasty", "great food"]):
            custom_msg = "Chef's Kiss! 👩‍🍳💋 We're framing this review!"
        elif any(x in lower_msg for x in ["staff", "service", "waiter", "waitress"]):
            custom_msg = "Give that staff member a raise! 🏆"
        elif "atmosphere" in lower_msg or "place" in lower_msg:
            custom_msg = "Vibes: Immaculate. ✨"
        else:
            custom_msg = "You just made our day! 😊"

    # Return JSON instead of HTML
    return {
        "prediction": prediction,
        "confidence": confidence,
        "custom_msg": custom_msg
    }

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    # Run with host 0.0.0.0 to be accessible externally
    uvicorn.run(app, host="0.0.0.0", port=port)