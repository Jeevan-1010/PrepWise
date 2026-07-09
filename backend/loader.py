"""
backend.loader

Handles dataset loading and validation for PrepWise.
"""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}


class DatasetLoaderError(Exception):
    """Raised when dataset loading fails."""


def validate_extension(filename: str) -> None:
    """
    Validate uploaded file extension.

    Args:
        filename: Uploaded file name.

    Raises:
        DatasetLoaderError: If extension is unsupported.
    """

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise DatasetLoaderError(
            f"Unsupported file format '{extension}'. "
            f"Supported formats: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )


def _read_file(file: BinaryIO, extension: str) -> pd.DataFrame:
    """
    Read dataset based on file extension.
    """

    if extension == ".csv":
        return pd.read_csv(file)

    if extension == ".xlsx":
        return pd.read_excel(file)

    raise DatasetLoaderError("Unsupported file type.")


def load_dataset(file: BinaryIO, filename: str) -> pd.DataFrame:
    """
    Load dataset into a pandas DataFrame.

    Args:
        file: Uploaded file object.
        filename: Original filename.

    Returns:
        Loaded DataFrame.

    Raises:
        DatasetLoaderError
    """

    validate_extension(filename)

    extension = Path(filename).suffix.lower()

    try:
        df = _read_file(file, extension)

    except Exception as exc:
        raise DatasetLoaderError(
            f"Failed to load dataset: {exc}"
        ) from exc

    if df.empty:
        raise DatasetLoaderError(
            "Uploaded dataset is empty."
        )

    if df.columns.duplicated().any():
        raise DatasetLoaderError(
            "Duplicate column names detected."
        )

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace(" ", "_")
    )

    return df


def get_dataset_info(df: pd.DataFrame) -> dict:
    """
    Return dataset metadata.
    """

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "memory_mb": round(
            df.memory_usage(deep=True).sum() / (1024 ** 2),
            2,
        ),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_columns": df.select_dtypes(include="number").columns.tolist(),
        "categorical_columns": df.select_dtypes(include="object").columns.tolist(),
        "datetime_columns": df.select_dtypes(
            include=["datetime", "datetimetz"]
        ).columns.tolist(),
    }