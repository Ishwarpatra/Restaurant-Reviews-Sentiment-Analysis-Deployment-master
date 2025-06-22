from flask import Flask, render_template, request

# Local modules for sentiment and RAG
from rag_helper import init_rag, retrieve_context
from sentiment_model import SentimentModel, classify_label

app = Flask(__name__)

# initialize RAG components and the sentiment model
init_rag()
sentiment_model = SentimentModel()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        # retrieve additional context using RAG
        context = retrieve_context(message)
        enriched_input = f"{message}\n{context}" if context else message

        label, score = sentiment_model.predict(enriched_input)
        final_prediction = classify_label(label, score)

        return render_template(
            'result.html',
            prediction=final_prediction,
            score=round(score, 3),
            raw_label=label
        )


if __name__ == '__main__':
    app.run(debug=True)

