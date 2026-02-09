# Importing essential libraries
from flask import Flask, render_template, request
import pickle

# Load the Multinomial Naive Bayes model and TfidfVectorizer object from disk
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, 'restaurant-sentiment-mnb-model.pkl')
vectorizer_path = os.path.join(script_dir, 'cv-transform.pkl')

classifier = pickle.load(open(model_path, 'rb'))
cv = pickle.load(open(vectorizer_path,'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            message = request.form['message']
            if not message.strip():  # Check if message is empty or just whitespace
                return render_template('result.html', prediction=None, error="Please enter a valid review.")
            
            data = [message]
            vect = cv.transform(data).toarray()
            
            # 1. Get Prediction AND Probability
            prediction = classifier.predict(vect)[0]
            proba = classifier.predict_proba(vect)[0] # Returns [prob_neg, prob_pos]
            
            # Calculate confidence score (0 to 100)
            confidence = round(max(proba) * 100, 2)
            
            # 2. "The Witty Chef" Logic
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

            return render_template('result.html', prediction=prediction, confidence=confidence, custom_msg=custom_msg)
            
        except Exception as e:
            return render_template('result.html', prediction=None, error=f"An error occurred: {str(e)}")

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    # Default to False in production
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(host='0.0.0.0', port=port, debug=debug_mode)