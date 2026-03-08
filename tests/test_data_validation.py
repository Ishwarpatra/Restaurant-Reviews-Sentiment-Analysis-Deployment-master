"""
test_data_validation.py - Tests for the Data Validation Module
===============================================================
Tests for data_validation.py covering file checks, column validation,
null detection, duplicate detection, class balance, and label validation.

Run:
    pytest tests/test_data_validation.py -v
"""

import sys
import os
import tempfile

import pytest
import pandas as pd

# Ensure project root is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.data_validation import (
    check_file_exists,
    check_required_columns,
    check_null_values,
    check_duplicates,
    check_class_balance,
    check_label_values,
    check_review_lengths,
    check_empty_reviews,
    validate_dataset,
)


# ── File Existence ───────────────────────────────────────────────────────


class TestCheckFileExists:
    """Tests for check_file_exists."""

    def test_existing_file(self, tmp_path):
        f = tmp_path / "test.tsv"
        f.write_text("Review\tLiked\nGood\t1\n")
        result = check_file_exists(str(f))
        assert result["passed"] is True

    def test_nonexistent_file(self):
        result = check_file_exists("/nonexistent/path/to/file.tsv")
        assert result["passed"] is False


# ── Required Columns ─────────────────────────────────────────────────────


class TestCheckRequiredColumns:
    """Tests for check_required_columns."""

    def test_all_columns_present(self):
        df = pd.DataFrame({"Review": ["test"], "Liked": [1]})
        result = check_required_columns(df)
        assert result["passed"] is True

    def test_missing_column(self):
        df = pd.DataFrame({"Review": ["test"]})
        result = check_required_columns(df)
        assert result["passed"] is False

    def test_custom_required_columns(self):
        df = pd.DataFrame({"text": ["test"], "label": [1]})
        result = check_required_columns(df, required={"text", "label"})
        assert result["passed"] is True


# ── Null Values ──────────────────────────────────────────────────────────


class TestCheckNullValues:
    """Tests for check_null_values."""

    def test_no_nulls(self):
        df = pd.DataFrame({"Review": ["good", "bad"], "Liked": [1, 0]})
        result = check_null_values(df)
        assert result["passed"] is True

    def test_with_nulls(self):
        df = pd.DataFrame({"Review": ["good", None], "Liked": [1, 0]})
        result = check_null_values(df)
        assert result["passed"] is False
        assert "1" in result["details"]


# ── Duplicates ───────────────────────────────────────────────────────────


class TestCheckDuplicates:
    """Tests for check_duplicates."""

    def test_no_duplicates(self):
        df = pd.DataFrame({"Review": ["good", "bad", "okay"]})
        result = check_duplicates(df)
        assert result["passed"] is True

    def test_with_duplicates(self):
        reviews = ["good"] * 50 + ["bad"] * 50
        df = pd.DataFrame({"Review": reviews})
        result = check_duplicates(df, threshold=0.05)
        assert result["passed"] is False

    def test_below_threshold(self):
        reviews = ["good", "good", "bad", "okay", "fine"] * 20
        df = pd.DataFrame({"Review": reviews})
        result = check_duplicates(df, threshold=0.99)
        assert result["passed"] is True


# ── Class Balance ────────────────────────────────────────────────────────


class TestCheckClassBalance:
    """Tests for check_class_balance."""

    def test_balanced_classes(self):
        df = pd.DataFrame({"Liked": [0, 0, 0, 1, 1, 1]})
        result = check_class_balance(df)
        assert result["passed"] is True

    def test_imbalanced_classes(self):
        df = pd.DataFrame({"Liked": [0] * 10 + [1] * 100})
        result = check_class_balance(df, max_ratio=2.0)
        assert result["passed"] is False

    def test_single_class(self):
        df = pd.DataFrame({"Liked": [1, 1, 1]})
        result = check_class_balance(df)
        assert result["passed"] is False


# ── Label Values ─────────────────────────────────────────────────────────


class TestCheckLabelValues:
    """Tests for check_label_values."""

    def test_valid_labels(self):
        df = pd.DataFrame({"Liked": [0, 1, 0, 1]})
        result = check_label_values(df)
        assert result["passed"] is True

    def test_invalid_labels(self):
        df = pd.DataFrame({"Liked": [0, 1, 2, -1]})
        result = check_label_values(df)
        assert result["passed"] is False

    def test_missing_column(self):
        df = pd.DataFrame({"Review": ["test"]})
        result = check_label_values(df)
        assert result["passed"] is False


# ── Review Lengths ───────────────────────────────────────────────────────


class TestCheckReviewLengths:
    """Tests for check_review_lengths."""

    def test_normal_lengths(self):
        df = pd.DataFrame({"Review": ["This is a normal review", "Another one here"]})
        result = check_review_lengths(df)
        assert result["passed"] is True

    def test_too_short_review(self):
        df = pd.DataFrame({"Review": ["OK", "This is fine"]})
        result = check_review_lengths(df, min_length=3)
        assert result["passed"] is False

    def test_too_long_review(self):
        df = pd.DataFrame({"Review": ["x" * 20000, "normal"]})
        result = check_review_lengths(df, max_length=10000)
        assert result["passed"] is False


# ── Empty Reviews ────────────────────────────────────────────────────────


class TestCheckEmptyReviews:
    """Tests for check_empty_reviews."""

    def test_no_empty_reviews(self):
        df = pd.DataFrame({"Review": ["good", "bad"]})
        result = check_empty_reviews(df)
        assert result["passed"] is True

    def test_with_empty_reviews(self):
        df = pd.DataFrame({"Review": ["good", "", "   "]})
        result = check_empty_reviews(df)
        assert result["passed"] is False


# ── Full Validation ──────────────────────────────────────────────────────


class TestValidateDataset:
    """Integration tests for validate_dataset."""

    def test_valid_dataset(self, tmp_path):
        """Create a valid TSV and run full validation."""
        f = tmp_path / "valid.tsv"
        rows = [f"Review {i}\t{i % 2}" for i in range(100)]
        f.write_text("Review\tLiked\n" + "\n".join(rows))

        report = validate_dataset(str(f), verbose=False)
        assert report["is_valid"] is True
        assert len(report["errors"]) == 0

    def test_nonexistent_file(self):
        report = validate_dataset("/no/such/file.tsv", verbose=False)
        assert report["is_valid"] is False

    def test_real_dataset(self):
        """Validate the actual project dataset if it exists."""
        dataset_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "Restaurant_Reviews.tsv",
        )
        if os.path.exists(dataset_path):
            report = validate_dataset(dataset_path, verbose=False)
            assert report["is_valid"] is True
            assert report["summary"]["total_rows"] == 1000
