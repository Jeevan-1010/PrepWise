"""
backend.utils

Shared utility functions for PrepWise.
"""

from __future__ import annotations

import logging
from datetime import datetime

import numpy as np
import pandas as pd


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("PrepWise")


# ---------------------------------------------------------
# Dataset Validation
# ---------------------------------------------------------

def validate_dataframe(df: pd.DataFrame) -> bool:
    """
    Validate DataFrame.
    """

    return isinstance(df, pd.DataFrame) and not df.empty


# ---------------------------------------------------------
# Dataset Quality Grade
# ---------------------------------------------------------

def quality_grade(score: float) -> str:
    """
    Convert quality score into grade.
    """

    if score >= 90:
        return "A+"

    if score >= 80:
        return "A"

    if score >= 70:
        return "B"

    if score >= 60:
        return "C"

    return "Needs Improvement"


# ---------------------------------------------------------
# Missing Value Summary
# ---------------------------------------------------------

def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return missing value summary.
    """

    missing = df.isna().sum()

    summary = pd.DataFrame(
        {
            "Column": missing.index,
            "Missing Values": missing.values,
            "Percentage": (
                missing / len(df) * 100
            ).round(2),
        }
    )

    return summary.sort_values(
        "Missing Values",
        ascending=False,
    )


# ---------------------------------------------------------
# Numerical Columns
# ---------------------------------------------------------

def numerical_columns(df: pd.DataFrame) -> list[str]:
    """
    Return numeric columns.
    """

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


# ---------------------------------------------------------
# Categorical Columns
# ---------------------------------------------------------

def categorical_columns(df: pd.DataFrame) -> list[str]:
    """
    Return categorical columns.
    """

    return df.select_dtypes(
        exclude=np.number
    ).columns.tolist()


# ---------------------------------------------------------
# Memory Usage
# ---------------------------------------------------------

def memory_usage(df: pd.DataFrame) -> float:
    """
    Dataset memory usage in MB.
    """

    return round(
        df.memory_usage(deep=True).sum()
        / (1024 ** 2),
        2,
    )


# ---------------------------------------------------------
# Current Timestamp
# ---------------------------------------------------------

def current_timestamp() -> str:
    """
    Return formatted timestamp.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# ---------------------------------------------------------
# Dataset Report
# ---------------------------------------------------------

def dataset_report(
    df: pd.DataFrame,
    quality_score: float,
) -> dict:
    """
    Generate dataset report.
    """

    return {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing Values": int(df.isna().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Memory (MB)": memory_usage(df),
        "Quality Score": quality_score,
        "Quality Grade": quality_grade(
            quality_score
        ),
        "Generated At": current_timestamp(),
    }


# ---------------------------------------------------------
# Safe Copy
# ---------------------------------------------------------

def safe_copy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a deep copy.
    """

    return df.copy(deep=True)


# ---------------------------------------------------------
# Normalize Column Names
# ---------------------------------------------------------

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize DataFrame column names.
    """

    copied = safe_copy(df)

    copied.columns = (
        copied.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return copied