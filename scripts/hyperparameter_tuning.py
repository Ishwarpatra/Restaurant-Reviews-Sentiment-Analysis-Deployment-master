"""
hyperparameter_tuning.py - Model Optimisation Script
=====================================================
Uses GridSearchCV and cross-validation to find optimal hyperparameters
for the Multinomial Naive Bayes sentiment classifier.

Usage:
    python hyperparameter_tuning.py

The script will:
    1. Load and preprocess the dataset
    2. Run GridSearchCV over alpha values and max_features
    3. Report cross-validation results
    4. Optionally save the best model
"""

import os
import pickle
import logging

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import (
    GridSearchCV,
    StratifiedKFold,
    cross_val_score,
)
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    make_scorer,
    f1_score,
    roc_auc_score,
)

from preprocess import preprocess_corpus

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(SCRIPT_DIR, "Restaurant_Reviews.tsv")
MODEL_PATH = os.path.join(SCRIPT_DIR, "restaurant-sentiment-mnb-model.pkl")
VECTORIZER_PATH = os.path.join(SCRIPT_DIR, "cv-transform.pkl")

# Hyperparameter search space
PARAM_GRID = {
    "tfidf__max_features": [500, 1000, 1500, 2000, None],
    "clf__alpha": [0.05, 0.1, 0.2, 0.5, 1.0, 2.0],
}

# Cross-validation configuration
CV_FOLDS = 5
RANDOM_STATE = 42


def load_and_preprocess() -> tuple:
    """Load the dataset and preprocess reviews.

    Returns:
        Tuple of (corpus, labels, dataframe).
    """
    print("=" * 70)
    print("HYPERPARAMETER TUNING PIPELINE")
    print("=" * 70)

    df = pd.read_csv(DATASET_PATH, delimiter="\t", quoting=3)
    print(f"\n[DATA] Loaded {len(df)} reviews")
    print(f"       Positive: {(df['Liked'] == 1).sum()} | "
          f"Negative: {(df['Liked'] == 0).sum()}")

    corpus = preprocess_corpus(df["Review"])
    y = df["Liked"].values

    print(f"[OK] Preprocessing complete ({len(corpus)} reviews)")
    return corpus, y, df


def run_grid_search(corpus: list, y: np.ndarray) -> GridSearchCV:
    """Run GridSearchCV to find optimal hyperparameters.

    Args:
        corpus: List of preprocessed review strings.
        y: Binary label array.

    Returns:
        Fitted GridSearchCV object.
    """
    print("\n" + "-" * 70)
    print("GRID SEARCH WITH CROSS-VALIDATION")
    print("-" * 70)
    print(f"  Folds: {CV_FOLDS}")
    print(f"  Scoring: F1 (weighted)")
    print(f"  Parameter grid:")
    for k, v in PARAM_GRID.items():
        print(f"    {k}: {v}")

    # Build sklearn pipeline
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", MultinomialNB()),
    ])

    # Stratified K-Fold ensures class balance in each fold
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    scorer = make_scorer(f1_score, average="weighted")

    grid_search = GridSearchCV(
        pipeline,
        PARAM_GRID,
        cv=cv,
        scoring=scorer,
        n_jobs=-1,  # Use all CPU cores
        verbose=1,
        return_train_score=True,
    )

    print("\n  Running search (this may take a moment)...\n")
    grid_search.fit(corpus, y)

    return grid_search


def report_results(grid_search: GridSearchCV, corpus: list, y: np.ndarray) -> None:
    """Print detailed results from GridSearchCV.

    Args:
        grid_search: Fitted GridSearchCV object.
        corpus: Preprocessed review strings.
        y: Labels.
    """
    print("\n" + "-" * 70)
    print("GRID SEARCH RESULTS")
    print("-" * 70)

    print(f"\n  Best parameters:")
    for k, v in grid_search.best_params_.items():
        label = str(v) if v is not None else "ALL (no limit)"
        print(f"    {k}: {label}")
    print(f"\n  Best CV F1-Score (weighted): {grid_search.best_score_:.4f}")

    # Top 5 parameter combinations
    results = pd.DataFrame(grid_search.cv_results_)
    results = results.sort_values("rank_test_score")

    print("\n  Top 5 parameter combinations:")
    print(f"  {'Rank':<6} {'Alpha':<8} {'Max Features':<15} {'Mean F1':<10} {'Std F1':<10}")
    print(f"  {'-'*6} {'-'*8} {'-'*15} {'-'*10} {'-'*10}")

    for _, row in results.head(5).iterrows():
        alpha = row["param_clf__alpha"]
        max_f = row["param_tfidf__max_features"]
        max_f_str = str(max_f) if max_f is not None else "ALL"
        print(
            f"  {int(row['rank_test_score']):<6} "
            f"{alpha:<8} "
            f"{max_f_str:<15} "
            f"{row['mean_test_score']:.4f}     "
            f"{row['std_test_score']:.4f}"
        )

    # Cross-validation scores for the best model
    print("\n" + "-" * 70)
    print("CROSS-VALIDATION DETAIL (BEST MODEL)")
    print("-" * 70)

    best_pipeline = grid_search.best_estimator_
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    # Multiple metrics
    for metric_name, scorer_fn in [
        ("F1 (weighted)", make_scorer(f1_score, average="weighted")),
        ("Accuracy", "accuracy"),
    ]:
        scores = cross_val_score(best_pipeline, corpus, y, cv=cv, scoring=scorer_fn)
        print(f"\n  {metric_name}:")
        for i, s in enumerate(scores, 1):
            print(f"    Fold {i}: {s:.4f}")
        print(f"    Mean:   {scores.mean():.4f} (+/- {scores.std() * 2:.4f})")


def save_best_model(grid_search: GridSearchCV) -> None:
    """Save the best model and vectoriser from GridSearchCV.

    Args:
        grid_search: Fitted GridSearchCV object.
    """
    print("\n" + "-" * 70)
    print("SAVING BEST MODEL")
    print("-" * 70)

    best = grid_search.best_estimator_
    vectoriser = best.named_steps["tfidf"]
    classifier = best.named_steps["clf"]

    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectoriser, f)
    print(f"  [OK] Vectoriser saved -> {VECTORIZER_PATH}")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(classifier, f)
    print(f"  [OK] Classifier saved -> {MODEL_PATH}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    corpus, y, df = load_and_preprocess()
    grid = run_grid_search(corpus, y)
    report_results(grid, corpus, y)

    # Ask before overwriting existing model files
    print()
    answer = input("Save the best model? This will overwrite existing .pkl files [y/N]: ")
    if answer.strip().lower() in ("y", "yes"):
        save_best_model(grid)
    else:
        print("  Model NOT saved.")

    print("\n" + "=" * 70)
    print("TUNING COMPLETE")
    print("=" * 70)
