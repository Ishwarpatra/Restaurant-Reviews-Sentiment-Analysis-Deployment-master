"""
Restaurant Reviews Sentiment Analyser – Training & Evaluation Script
====================================================================
Trains a Multinomial Naive Bayes classifier on restaurant reviews.

Improvements over the original:
  • Lemmatisation (WordNetLemmatizer) instead of stemming
  • TF-IDF vectorisation instead of raw Bag-of-Words
  • Automated vocabulary size analysis to choose optimal max_features
  • Full evaluation metrics (Classification Report, Confusion Matrix,
    Accuracy, F1-Score, ROC-AUC)
  • Cross-platform path handling via os.path.join
"""

# ── Imports ──────────────────────────────────────────────────────────────────
import os
import re
import pickle

import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    f1_score,
    roc_auc_score,
)

# ── NLTK data ────────────────────────────────────────────────────────────────
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(SCRIPT_DIR, "Restaurant_Reviews.tsv")
MODEL_PATH = os.path.join(SCRIPT_DIR, "restaurant-sentiment-mnb-model.pkl")
VECTORIZER_PATH = os.path.join(SCRIPT_DIR, "cv-transform.pkl")

# ── 1. Load dataset ─────────────────────────────────────────────────────────
print("=" * 70)
print("RESTAURANT REVIEWS SENTIMENT ANALYSER – TRAINING PIPELINE")
print("=" * 70)

df = pd.read_csv(DATASET_PATH, delimiter="\t", quoting=3)
print(f"\n[DATA] Dataset loaded: {len(df)} reviews")
print(f"       Positive: {(df['Liked'] == 1).sum()} | Negative: {(df['Liked'] == 0).sum()}")

# ── 2. Text preprocessing ───────────────────────────────────────────────────
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

corpus = []
for review_text in df["Review"]:
    # Remove special characters, lowercase, tokenise
    cleaned = re.sub(r"[^a-zA-Z]", " ", str(review_text)).lower().split()
    # Remove stop-words & lemmatise
    cleaned = [lemmatizer.lemmatize(w) for w in cleaned if w not in stop_words]
    corpus.append(" ".join(cleaned))

print(f"[OK] Preprocessing complete ({len(corpus)} reviews cleaned)")

# ── 3. Vocabulary size analysis ──────────────────────────────────────────────
print("\n" + "-" * 70)
print("VOCABULARY SIZE ANALYSIS")
print("-" * 70)

y = df["Liked"].values
candidates = [500, 1000, 1500, 2000, 2500, 3000, None]
best_score = 0
best_features = None

for n in candidates:
    vec = TfidfVectorizer(max_features=n)
    X_temp = vec.fit_transform(corpus).toarray()
    X_tr, X_te, y_tr, y_te = train_test_split(
        X_temp, y, test_size=0.20, random_state=0
    )
    clf = MultinomialNB(alpha=0.2)
    clf.fit(X_tr, y_tr)
    score = f1_score(y_te, clf.predict(X_te), average="weighted")
    label = str(n) if n else "ALL"
    print(f"   max_features={label:>5s}  ->  F1-Score (weighted): {score:.4f}")
    if score > best_score:
        best_score = score
        best_features = n

label = str(best_features) if best_features else "ALL (no limit)"
print(f"\n>> Optimal vocabulary size: {label}  (F1 = {best_score:.4f})")

# ── 4. Final model training with optimal features ───────────────────────────
print("\n" + "-" * 70)
print("TRAINING FINAL MODEL")
print("-" * 70)

tfidf = TfidfVectorizer(max_features=best_features)
X = tfidf.fit_transform(corpus).toarray()

actual_vocab_size = len(tfidf.vocabulary_)
print(f"   Vocabulary size: {actual_vocab_size}")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=0
)
print(f"   Training set: {len(X_train)} | Test set: {len(X_test)}")

classifier = MultinomialNB(alpha=0.2)
classifier.fit(X_train, y_train)
print("[OK] Model training complete")

# ── 5. Evaluation metrics ───────────────────────────────────────────────────
print("\n" + "-" * 70)
print("MODEL EVALUATION")
print("-" * 70)

y_pred = classifier.predict(X_test)
y_proba = classifier.predict_proba(X_test)[:, 1]

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Negative", "Positive"]))

print("Confusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(f"   TN={cm[0][0]:>4d}  FP={cm[0][1]:>4d}")
print(f"   FN={cm[1][0]:>4d}  TP={cm[1][1]:>4d}")

acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average="weighted")
roc = roc_auc_score(y_test, y_proba)

print(f"\n   Accuracy : {acc:.4f}")
print(f"   F1-Score : {f1:.4f}")
print(f"   ROC-AUC  : {roc:.4f}")

# ── 6. Save artefacts ───────────────────────────────────────────────────────
print("\n" + "-" * 70)
print("SAVING ARTEFACTS")
print("-" * 70)

with open(VECTORIZER_PATH, "wb") as f:
    pickle.dump(tfidf, f)
print(f"   [OK] Vectoriser saved -> {VECTORIZER_PATH}")

with open(MODEL_PATH, "wb") as f:
    pickle.dump(classifier, f)
print(f"   [OK] Model saved      -> {MODEL_PATH}")

print("\n" + "=" * 70)
print("PIPELINE COMPLETE")
print("=" * 70)