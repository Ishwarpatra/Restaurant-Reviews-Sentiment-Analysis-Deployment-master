"""
data_validation.py - Data Quality Validation Module
=====================================================
Validates the restaurant reviews dataset before training or inference.
Checks for nulls, duplicates, class imbalance, encoding issues, and
structural integrity.

Usage:
    from data_validation import validate_dataset

    report = validate_dataset("Restaurant_Reviews.tsv")
    if not report["is_valid"]:
        print("Validation failed:", report["errors"])
"""

import os
import logging
from typing import Any, Dict, List, Optional

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Configuration defaults
# ---------------------------------------------------------------------------
DEFAULT_REQUIRED_COLUMNS = {"Review", "Liked"}
DEFAULT_MAX_IMBALANCE_RATIO = 3.0  # majority / minority < 3x
DEFAULT_MIN_REVIEW_LENGTH = 3  # characters
DEFAULT_MAX_REVIEW_LENGTH = 10_000
DEFAULT_DUPLICATE_THRESHOLD = 0.10  # warn if >10% duplicates


# ---------------------------------------------------------------------------
# Validation functions
# ---------------------------------------------------------------------------


def check_file_exists(filepath: str) -> Dict[str, Any]:
    """Check that the dataset file exists and is readable."""
    result = {"check": "file_exists", "passed": False, "details": ""}
    if not os.path.isfile(filepath):
        result["details"] = f"File not found: {filepath}"
        return result
    size_kb = os.path.getsize(filepath) / 1024
    result["passed"] = True
    result["details"] = f"File exists ({size_kb:.1f} KB)"
    return result


def check_required_columns(
    df: pd.DataFrame, required: Optional[set] = None
) -> Dict[str, Any]:
    """Verify all required columns are present."""
    required = required or DEFAULT_REQUIRED_COLUMNS
    result = {"check": "required_columns", "passed": False, "details": ""}
    missing = required - set(df.columns)
    if missing:
        result["details"] = f"Missing columns: {missing}"
    else:
        result["passed"] = True
        result["details"] = f"All required columns present: {sorted(required)}"
    return result


def check_null_values(df: pd.DataFrame) -> Dict[str, Any]:
    """Check for null/NaN values in the dataset."""
    result = {"check": "null_values", "passed": False, "details": ""}
    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()
    if total_nulls > 0:
        breakdown = {col: int(n) for col, n in null_counts.items() if n > 0}
        result["details"] = f"Found {total_nulls} null(s): {breakdown}"
    else:
        result["passed"] = True
        result["details"] = "No null values found"
    return result


def check_duplicates(
    df: pd.DataFrame,
    column: str = "Review",
    threshold: float = DEFAULT_DUPLICATE_THRESHOLD,
) -> Dict[str, Any]:
    """Check for duplicate reviews."""
    result = {"check": "duplicates", "passed": False, "details": ""}
    if column not in df.columns:
        result["details"] = f"Column '{column}' not found for duplicate check"
        return result

    n_dupes = df[column].duplicated().sum()
    dupe_ratio = n_dupes / len(df) if len(df) > 0 else 0

    if dupe_ratio > threshold:
        result["details"] = (
            f"High duplicate rate: {n_dupes} duplicates "
            f"({dupe_ratio:.1%}) exceeds threshold ({threshold:.0%})"
        )
    else:
        result["passed"] = True
        result["details"] = f"{n_dupes} duplicate(s) ({dupe_ratio:.1%})"
    return result


def check_class_balance(
    df: pd.DataFrame,
    label_column: str = "Liked",
    max_ratio: float = DEFAULT_MAX_IMBALANCE_RATIO,
) -> Dict[str, Any]:
    """Check class distribution for severe imbalance."""
    result = {"check": "class_balance", "passed": False, "details": ""}
    if label_column not in df.columns:
        result["details"] = f"Label column '{label_column}' not found"
        return result

    counts = df[label_column].value_counts()
    if len(counts) < 2:
        result["details"] = f"Only {len(counts)} class(es) found; expected 2"
        return result

    majority = counts.max()
    minority = counts.min()
    ratio = majority / minority if minority > 0 else float("inf")

    distribution = {str(k): int(v) for k, v in counts.items()}
    if ratio > max_ratio:
        result["details"] = (
            f"Imbalanced classes (ratio {ratio:.2f}x): {distribution}"
        )
    else:
        result["passed"] = True
        result["details"] = (
            f"Balanced classes (ratio {ratio:.2f}x): {distribution}"
        )
    return result


def check_label_values(
    df: pd.DataFrame, label_column: str = "Liked"
) -> Dict[str, Any]:
    """Ensure labels contain only expected values (0 and 1)."""
    result = {"check": "label_values", "passed": False, "details": ""}
    if label_column not in df.columns:
        result["details"] = f"Label column '{label_column}' not found"
        return result

    unique_vals = set(df[label_column].dropna().unique())
    expected = {0, 1}

    if unique_vals == expected:
        result["passed"] = True
        result["details"] = f"Labels are binary: {sorted(unique_vals)}"
    else:
        unexpected = unique_vals - expected
        result["details"] = f"Unexpected label values: {unexpected}"
    return result


def check_review_lengths(
    df: pd.DataFrame,
    column: str = "Review",
    min_length: int = DEFAULT_MIN_REVIEW_LENGTH,
    max_length: int = DEFAULT_MAX_REVIEW_LENGTH,
) -> Dict[str, Any]:
    """Check for extremely short or long reviews."""
    result = {"check": "review_lengths", "passed": False, "details": ""}
    if column not in df.columns:
        result["details"] = f"Column '{column}' not found"
        return result

    lengths = df[column].astype(str).str.len()
    too_short = (lengths < min_length).sum()
    too_long = (lengths > max_length).sum()

    stats = {
        "min": int(lengths.min()),
        "max": int(lengths.max()),
        "mean": round(float(lengths.mean()), 1),
        "too_short": int(too_short),
        "too_long": int(too_long),
    }

    if too_short > 0 or too_long > 0:
        result["details"] = (
            f"{too_short} review(s) shorter than {min_length} chars, "
            f"{too_long} review(s) longer than {max_length} chars. "
            f"Stats: {stats}"
        )
    else:
        result["passed"] = True
        result["details"] = f"All reviews within length bounds. Stats: {stats}"
    return result


def check_empty_reviews(
    df: pd.DataFrame, column: str = "Review"
) -> Dict[str, Any]:
    """Check for empty or whitespace-only reviews."""
    result = {"check": "empty_reviews", "passed": False, "details": ""}
    if column not in df.columns:
        result["details"] = f"Column '{column}' not found"
        return result

    empty_mask = df[column].astype(str).str.strip().eq("")
    n_empty = empty_mask.sum()

    if n_empty > 0:
        result["details"] = f"Found {n_empty} empty/whitespace-only review(s)"
    else:
        result["passed"] = True
        result["details"] = "No empty reviews"
    return result


# ---------------------------------------------------------------------------
# Main validation orchestrator
# ---------------------------------------------------------------------------


def validate_dataset(
    filepath: str,
    *,
    required_columns: Optional[set] = None,
    delimiter: str = "\t",
    max_imbalance_ratio: float = DEFAULT_MAX_IMBALANCE_RATIO,
    verbose: bool = True,
) -> Dict[str, Any]:
    """Run all validation checks on the dataset file.

    Args:
        filepath: Path to the TSV/CSV dataset file.
        required_columns: Set of column names that must be present.
        delimiter: Column delimiter (default: tab for TSV).
        max_imbalance_ratio: Maximum allowed majority/minority class ratio.
        verbose: Whether to print a formatted report.

    Returns:
        Dictionary with "is_valid", "checks" list, "errors" list, and "warnings".
    """
    report: Dict[str, Any] = {
        "is_valid": True,
        "checks": [],
        "errors": [],
        "warnings": [],
        "summary": {},
    }

    # --- File existence ---
    file_check = check_file_exists(filepath)
    report["checks"].append(file_check)
    if not file_check["passed"]:
        report["is_valid"] = False
        report["errors"].append(file_check["details"])
        if verbose:
            _print_report(report)
        return report

    # --- Load dataset ---
    try:
        df = pd.read_csv(filepath, delimiter=delimiter, quoting=3)
    except Exception as exc:
        error_msg = f"Failed to load dataset: {exc}"
        report["is_valid"] = False
        report["errors"].append(error_msg)
        report["checks"].append(
            {"check": "load_dataset", "passed": False, "details": error_msg}
        )
        if verbose:
            _print_report(report)
        return report

    report["summary"]["total_rows"] = len(df)
    report["summary"]["total_columns"] = len(df.columns)
    report["summary"]["columns"] = list(df.columns)

    # --- Run all checks ---
    checks = [
        check_required_columns(df, required_columns),
        check_null_values(df),
        check_duplicates(df),
        check_class_balance(df, max_ratio=max_imbalance_ratio),
        check_label_values(df),
        check_review_lengths(df),
        check_empty_reviews(df),
    ]

    for check in checks:
        report["checks"].append(check)
        if not check["passed"]:
            # Distinguish errors (critical) from warnings (non-critical)
            if check["check"] in ("required_columns", "label_values"):
                report["is_valid"] = False
                report["errors"].append(check["details"])
            else:
                report["warnings"].append(check["details"])

    if verbose:
        _print_report(report)

    return report


# ---------------------------------------------------------------------------
# Pretty-print helper
# ---------------------------------------------------------------------------

_PASS = "[PASS]"
_FAIL = "[FAIL]"
_WARN = "[WARN]"


def _print_report(report: Dict[str, Any]) -> None:
    """Print a formatted validation report to stdout."""
    print()
    print("=" * 70)
    print("DATA VALIDATION REPORT")
    print("=" * 70)

    if "total_rows" in report.get("summary", {}):
        s = report["summary"]
        print(f"  Dataset: {s['total_rows']} rows x {s['total_columns']} columns")
        print(f"  Columns: {s['columns']}")

    print()
    for check in report["checks"]:
        status = _PASS if check["passed"] else _FAIL
        print(f"  {status}  {check['check']}: {check['details']}")

    print()
    if report["is_valid"]:
        print("  RESULT: Dataset is VALID")
    else:
        print("  RESULT: Dataset has CRITICAL issues")
        for err in report["errors"]:
            print(f"    ERROR: {err}")

    if report["warnings"]:
        print()
        for warn in report["warnings"]:
            print(f"    WARNING: {warn}")

    print("=" * 70)
    print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_path = os.path.join(script_dir, "Restaurant_Reviews.tsv")
    filepath = sys.argv[1] if len(sys.argv) > 1 else default_path

    report = validate_dataset(filepath)

    # Exit with non-zero status if validation failed
    sys.exit(0 if report["is_valid"] else 1)
