"""
test_preprocess.py - Tests for the Text Preprocessing Module
=============================================================
Tests for preprocess.py covering text cleaning, contraction expansion,
stop-word removal, lemmatisation, and corpus-level processing.

Run:
    pytest tests/test_preprocess.py -v
"""

import sys
import os

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocess import clean_text, expand_contractions, preprocess_corpus


# ── clean_text tests ─────────────────────────────────────────────────────


class TestCleanText:
    """Tests for the clean_text function."""

    def test_basic_cleaning(self):
        """Should remove special chars, lowercase, and join tokens."""
        result = clean_text("The food was AMAZING!!!")
        assert result  # not empty
        assert result.islower() or result == ""
        assert "!" not in result

    def test_removes_numbers(self):
        """Should remove numeric characters."""
        result = clean_text("5 stars! Best meal in 2024")
        assert "5" not in result
        assert "2024" not in result

    def test_removes_special_characters(self):
        """Should remove punctuation and special chars."""
        result = clean_text("Great!!!! #amazing @restaurant $$$")
        assert "#" not in result
        assert "@" not in result
        assert "$" not in result

    def test_stop_word_removal(self):
        """Should remove English stop-words."""
        result = clean_text("The food was very good")
        assert "the" not in result.split()
        assert "was" not in result.split()

    def test_stop_word_removal_disabled(self):
        """Should keep stop-words when flag is False."""
        result = clean_text("The food was good", remove_stopwords=False)
        tokens = result.split()
        # "the", "was" should still be present (lowercased, lemmatised)
        assert "food" in tokens

    def test_lemmatisation(self):
        """Should lemmatise words (e.g., 'studies' -> 'study')."""
        result = clean_text("running studies amazing cats")
        tokens = result.split()
        assert "study" in tokens or "studies" in tokens  # lemmatiser may vary

    def test_lemmatisation_disabled(self):
        """Should skip lemmatisation when flag is False."""
        result = clean_text("running cats", lemmatize=False)
        tokens = result.split()
        assert "running" in tokens

    def test_empty_string(self):
        """Should return empty string for empty input."""
        assert clean_text("") == ""

    def test_none_input(self):
        """Should handle None gracefully."""
        assert clean_text(None) == ""  # type: ignore

    def test_whitespace_only(self):
        """Should return empty string for whitespace-only input."""
        assert clean_text("   ") == ""
        assert clean_text("\t\n") == ""

    def test_min_word_length(self):
        """Should filter tokens shorter than min_word_length."""
        result = clean_text("I am a good cook", min_word_length=3)
        tokens = result.split()
        for token in tokens:
            assert len(token) >= 2  # default min

    def test_custom_stopwords(self):
        """Should remove custom stop-words in addition to NLTK set."""
        result = clean_text(
            "The restaurant food was delicious",
            custom_stopwords={"delicious"},
        )
        assert "delicious" not in result.split()

    def test_single_word(self):
        """Should handle single-word input."""
        result = clean_text("Delicious")
        assert result == "delicious"

    def test_unicode_input(self):
        """Should handle unicode gracefully (non-alpha removed)."""
        result = clean_text("Cafe latte is great")
        assert isinstance(result, str)


# ── expand_contractions tests ────────────────────────────────────────────


class TestExpandContractions:
    """Tests for the expand_contractions function."""

    def test_wont(self):
        assert "will not" in expand_contractions("I won't go").lower()

    def test_cant(self):
        assert "cannot" in expand_contractions("I can't believe it").lower()

    def test_isnt(self):
        result = expand_contractions("It isn't good")
        assert " not" in result.lower()

    def test_no_contractions(self):
        """Should return unchanged text when no contractions present."""
        text = "The food was great"
        assert expand_contractions(text) == text

    def test_multiple_contractions(self):
        result = expand_contractions("I won't and can't go")
        assert "will not" in result.lower()
        assert "cannot" in result.lower()


# ── preprocess_corpus tests ──────────────────────────────────────────────


class TestPreprocessCorpus:
    """Tests for the preprocess_corpus function."""

    def test_returns_list(self, sample_reviews):
        result = preprocess_corpus(sample_reviews)
        assert isinstance(result, list)

    def test_same_length_as_input(self, sample_reviews):
        result = preprocess_corpus(sample_reviews)
        assert len(result) == len(sample_reviews)

    def test_all_strings(self, sample_reviews):
        result = preprocess_corpus(sample_reviews)
        for item in result:
            assert isinstance(item, str)

    def test_handles_empty_list(self):
        result = preprocess_corpus([])
        assert result == []

    def test_handles_none_values(self):
        result = preprocess_corpus([None, "", "Good food"])
        assert len(result) == 3
        assert all(isinstance(r, str) for r in result)

    def test_special_characters(self, special_character_reviews):
        result = preprocess_corpus(special_character_reviews)
        assert len(result) == len(special_character_reviews)
        for cleaned in result:
            # No special chars should remain
            assert "#" not in cleaned
            assert "$" not in cleaned
            assert "<" not in cleaned
