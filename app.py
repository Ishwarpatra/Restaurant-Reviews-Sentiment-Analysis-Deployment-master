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
            my_prediction = classifier.predict(vect)
            return render_template('result.html', prediction=my_prediction)
        except Exception as e:
            return render_template('result.html', prediction=None, error=f"An error occurred during prediction: {str(e)}")

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    # Default to False in production
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(host='0.0.0.0', port=port, debug=debug_mode)