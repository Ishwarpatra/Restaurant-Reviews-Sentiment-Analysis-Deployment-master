# Model Documentation

## Overview

This project uses a **Multinomial Naive Bayes (MNB)** classifier for binary sentiment
classification of restaurant reviews. The model predicts whether a given review is
**positive** (1) or **negative** (0).

---

## Architecture

```
Raw Text
    |
    v
Text Cleaning (regex: remove non-alphabetic characters)
    |
    v
Lowercase Conversion
    |
    v
Tokenisation (whitespace split)
    |
    v
Stop-word Removal (NLTK English stop-words)
    |
    v
Lemmatisation (WordNetLemmatizer)
    |
    v
TF-IDF Vectorisation (Term Frequency-Inverse Document Frequency)
    |
    v
Multinomial Naive Bayes Classifier (alpha=0.2)
    |
    v
Prediction: Positive (1) / Negative (0) + Confidence Score
```

---

## Why Multinomial Naive Bayes?

| Criterion                | MNB Advantage                                              |
| ------------------------ | ---------------------------------------------------------- |
| **Speed**                | Trains in milliseconds, even on modest hardware            |
| **Interpretability**     | Probability-based predictions with calibrated confidence   |
| **Small Data**           | Performs well on 1,000-sample datasets without overfitting  |
| **TF-IDF Compatibility** | Naturally handles term-frequency feature representations   |
| **Deployment Footprint** | Tiny model file (~48 KB), ideal for serverless/containers  |

### Alternatives Considered

| Model       | Pros                            | Cons (for this use case)                      |
| ----------- | ------------------------------- | --------------------------------------------- |
| **SVM**     | Strong on high-dimensional data | Slower training, harder to tune                |
| **LSTM**    | Captures word order             | Overkill for 1K samples, needs GPU             |
| **BERT**    | State-of-the-art NLP            | 400MB+ model, cold start latency, needs GPU    |
| **LogReg**  | Good baseline                   | Similar performance to MNB, less interpretable |

---

## Hyperparameters

| Parameter          | Value         | Rationale                                        |
| ------------------ | ------------- | ------------------------------------------------ |
| `alpha`            | 0.2           | Laplace smoothing; lower values reduce bias       |
| `max_features`     | Auto-selected | Chosen via F1-score analysis across candidates    |
| `test_size`        | 0.20          | 80/20 train-test split                            |
| `random_state`     | 0             | Reproducibility                                   |

### Vocabulary Size Analysis

The training script evaluates these candidate vocabulary sizes and selects the one
with the highest weighted F1-score:

```
max_features=  500  ->  F1-Score (weighted): ~0.77
max_features= 1000  ->  F1-Score (weighted): ~0.78
max_features= 1500  ->  F1-Score (weighted): ~0.78
max_features= 2000  ->  F1-Score (weighted): ~0.77
max_features= 2500  ->  F1-Score (weighted): ~0.77
max_features= 3000  ->  F1-Score (weighted): ~0.77
max_features=  ALL  ->  F1-Score (weighted): ~0.77
```

---

## Preprocessing Pipeline

### 1. Text Cleaning

```python
cleaned = re.sub(r"[^a-zA-Z]", " ", review_text).lower().split()
```

- Removes all non-alphabetic characters (numbers, punctuation, emojis)
- Converts to lowercase
- Splits into tokens

### 2. Stop-word Removal

Uses the NLTK English stop-words list (179 words) to remove common
words that add noise (e.g., "the", "is", "at").

### 3. Lemmatisation

```python
lemmatizer = WordNetLemmatizer()
cleaned = [lemmatizer.lemmatize(w) for w in cleaned if w not in stop_words]
```

Lemmatisation is preferred over stemming because it produces valid dictionary
words (e.g., "better" -> "good") rather than truncated stems (e.g., "studies" -> "studi").

### 4. TF-IDF Vectorisation

- **Term Frequency (TF)**: How often a word appears in a document
- **Inverse Document Frequency (IDF)**: Penalises words that appear across many documents
- Result: A sparse matrix where important, discriminative words have higher weights

---

## Feature Extraction Details

| Property               | Value                                       |
| ---------------------- | ------------------------------------------- |
| Vectoriser Type        | `TfidfVectorizer` (scikit-learn)             |
| max_features           | Auto-selected (see vocabulary analysis)      |
| Vocabulary Size        | Typically ~1,000-1,500 features              |
| Sparse Representation  | Converted to dense array for MNB             |

---

## Evaluation Metrics

The training script (`Restaurant Reviews Sentiment Analyser - Deployment.py`)
outputs a full evaluation suite:

### Classification Report

```
              precision    recall  f1-score   support

    Negative       0.XX      0.XX      0.XX       XXX
    Positive       0.XX      0.XX      0.XX       XXX

    accuracy                           0.XX       200
   macro avg       0.XX      0.XX      0.XX       200
weighted avg       0.XX      0.XX      0.XX       200
```

### Confusion Matrix

```
   TN=  XX  FP=  XX
   FN=  XX  TP=  XX
```

| Metric               | Description                                         |
| -------------------- | --------------------------------------------------- |
| **Accuracy**         | Overall correctness (TP + TN) / Total               |
| **Precision**        | Of predicted positives, how many are correct         |
| **Recall**           | Of actual positives, how many were detected          |
| **F1-Score**         | Harmonic mean of precision and recall                |
| **ROC-AUC**         | Area under the Receiver Operating Characteristic curve |

### Interpreting Results

- **Accuracy ~77-79%**: Reasonable for 1,000 samples with a simple model
- **ROC-AUC ~0.84-0.86**: Good discrimination between classes
- **Balanced F1**: Dataset is balanced (500 positive, 500 negative), so F1
  closely tracks accuracy

---

## Dataset

| Property       | Value                          |
| -------------- | ------------------------------ |
| Source         | `Restaurant_Reviews.tsv`        |
| Format         | Tab-separated (TSV)            |
| Samples        | 1,000 reviews                  |
| Columns        | `Review` (text), `Liked` (0/1) |
| Class Balance  | 500 positive, 500 negative     |

---

## Model Artefacts

| File                               | Size   | Description                    |
| ---------------------------------- | ------ | ------------------------------ |
| `restaurant-sentiment-mnb-model.pkl` | ~48 KB | Trained MNB classifier         |
| `cv-transform.pkl`                  | ~64 KB | Fitted TF-IDF vectoriser       |

### Retraining

```bash
python "Restaurant Reviews Sentiment Analyser - Deployment.py"
```

This will:
1. Load and preprocess the dataset
2. Run vocabulary size analysis
3. Train the final model with optimal features
4. Print full evaluation metrics
5. Overwrite the `.pkl` artefact files

---

## Limitations

1. **Small Dataset**: 1,000 reviews limits generalisation to unseen domains
2. **Binary Classification**: No neutral/mixed sentiment category
3. **English Only**: Stop-word removal and lemmatisation are English-specific
4. **No Context**: Bag-of-words approach loses word order and context
5. **Domain Specific**: Trained only on restaurant reviews; may not transfer
   to other review domains (hotels, products, etc.)

## Future Improvements

- Fine-tune a pre-trained transformer (e.g., DistilBERT) for better accuracy
- Add multi-class sentiment (positive/neutral/negative)
- Expand dataset with augmentation techniques
- Add aspect-based sentiment analysis (food, service, ambiance)
- Implement online learning for continuous model updates
