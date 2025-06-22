import re
from typing import Tuple

try:
    from transformers import pipeline
except ImportError:
    pipeline = None

# Pre-compiled regular expression for handling negation like "not good".
NEGATION_PATTERN = re.compile(r"\b(?:not|no|n't)\s+(\w+)", re.IGNORECASE)


class SentimentModel:
    def __init__(self):
        if pipeline is None:
            self.model = None
        else:
            self.model = pipeline("sentiment-analysis")

    @staticmethod
    def _handle_negation(text: str) -> str:
        def replacer(match: re.Match) -> str:
            return match.group(0).replace(" ", "_")

        return NEGATION_PATTERN.sub(replacer, text)

    def predict(self, text: str) -> Tuple[str, float]:
        """Return (label, score) for the provided text."""
        if self.model is None:
            return "neutral", 0.0
        processed = self._handle_negation(text)
        result = self.model(processed)[0]
        label = result["label"].lower()
        score = float(result["score"])
        return label, score


# Classification thresholds
def classify_label(label: str, score: float) -> str:
    """Map model output to positive/negative/neutral labels with thresholds."""
    if label == "positive" and score >= 0.6:
        return "positive"
    if label == "negative" and score >= 0.6:
        return "negative"
    return "neutral"

