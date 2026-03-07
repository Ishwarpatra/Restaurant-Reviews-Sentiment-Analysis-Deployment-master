"""
preprocess.py - Standalone Text Preprocessing Module
=====================================================
Reusable text cleaning and tokenisation pipeline for restaurant review
sentiment analysis. Used by the training script and can be imported by
any inference or data-exploration code.

Usage:
    from preprocess import clean_text, preprocess_corpus

    # Single review
    cleaned = clean_text("The food was AMAZING!!! Best pasta ever :)")

    # Full DataFrame column
    corpus = preprocess_corpus(df["Review"])
"""

import re
import logging
from typing import List, Optional

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# ---------------------------------------------------------------------------
# Ensure NLTK resources are available
# ---------------------------------------------------------------------------
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level singletons (initialised once)
# ---------------------------------------------------------------------------
_lemmatizer = WordNetLemmatizer()
_stop_words: set = set(stopwords.words("english"))

# Characters to preserve: only alphabetic; everything else becomes a space
_NON_ALPHA_RE = re.compile(r"[^a-zA-Z]")

# Common contractions to expand before cleaning
_CONTRACTIONS = {
    "won't": "will not",
    "can't": "cannot",
    "n't": " not",
    "'re": " are",
    "'s": " is",
    "'d": " would",
    "'ll": " will",
    "'ve": " have",
    "'m": " am",
}
_CONTRACTION_RE = re.compile(
    "(" + "|".join(re.escape(k) for k in _CONTRACTIONS) + ")",
    flags=re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def expand_contractions(text: str) -> str:
    """Expand common English contractions.

    Examples:
        >>> expand_contractions("I won't go, can't believe it")
        "I will not go, cannot believe it"
    """

    def _replace(match: re.Match) -> str:
        return _CONTRACTIONS.get(match.group(0).lower(), match.group(0))

    return _CONTRACTION_RE.sub(_replace, text)


def clean_text(
    text: str,
    *,
    remove_stopwords: bool = True,
    lemmatize: bool = True,
    expand_contraction: bool = True,
    min_word_length: int = 2,
    custom_stopwords: Optional[set] = None,
) -> str:
    """Clean a single review string and return a space-joined token string.

    Pipeline:
        1. Expand contractions (optional)
        2. Remove non-alphabetic characters
        3. Lowercase
        4. Tokenise (whitespace split)
        5. Remove stop-words (optional)
        6. Filter by minimum word length
        7. Lemmatise (optional)

    Args:
        text: Raw review text.
        remove_stopwords: Whether to remove NLTK English stop-words.
        lemmatize: Whether to apply WordNet lemmatisation.
        expand_contraction: Whether to expand contractions first.
        min_word_length: Minimum number of characters for a token to be kept.
        custom_stopwords: Additional stop-words to remove beyond the NLTK set.

    Returns:
        Cleaned, space-joined string.
    """
    if not text or not isinstance(text, str):
        return ""

    # 1. Expand contractions
    if expand_contraction:
        text = expand_contractions(text)

    # 2. Remove non-alphabetic chars + 3. Lowercase + 4. Tokenise
    tokens = _NON_ALPHA_RE.sub(" ", text).lower().split()

    # 5. Stop-word removal
    if remove_stopwords:
        sw = _stop_words | (custom_stopwords or set())
        tokens = [w for w in tokens if w not in sw]

    # 6. Minimum word length filter
    if min_word_length > 1:
        tokens = [w for w in tokens if len(w) >= min_word_length]

    # 7. Lemmatise
    if lemmatize:
        tokens = [_lemmatizer.lemmatize(w) for w in tokens]

    return " ".join(tokens)


def preprocess_corpus(
    texts,
    **kwargs,
) -> List[str]:
    """Apply ``clean_text`` to an iterable of review strings.

    Args:
        texts: Iterable of raw review strings (e.g. pandas Series).
        **kwargs: Forwarded to ``clean_text``.

    Returns:
        List of cleaned strings, one per input review.
    """
    corpus = []
    error_count = 0
    for i, text in enumerate(texts):
        try:
            corpus.append(clean_text(str(text), **kwargs))
        except Exception:
            logger.warning("Failed to preprocess review at index %d", i)
            corpus.append("")
            error_count += 1

    if error_count:
        logger.warning(
            "Preprocessing finished with %d error(s) out of %d reviews.",
            error_count,
            len(corpus),
        )
    else:
        logger.info("Preprocessed %d reviews successfully.", len(corpus))

    return corpus


# ---------------------------------------------------------------------------
# CLI entry point for quick testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo_reviews = [
        "The food was AMAZING!!! Best pasta ever :)",
        "Terrible service. Had to wait 2 hours for cold soup.",
        "It's okay, nothing special. Won't come back.",
        "",
        None,
    ]

    print("=" * 60)
    print("PREPROCESSING DEMO")
    print("=" * 60)
    for raw in demo_reviews:
        cleaned = clean_text(str(raw) if raw else "")
        print(f"  RAW: {raw!r}")
        print(f"  OUT: {cleaned!r}")
        print()
