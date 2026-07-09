"""
backend.exporter

Exports cleaned datasets and analysis reports.
"""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd


SUPPORTED_EXPORTS = {".csv", ".xlsx"}


class ExportError(Exception):
    """Raised when exporting fails."""


def export_csv(df: pd.DataFrame) -> bytes:
    """
    Export DataFrame as CSV.

    Args:
        df: DataFrame to export.

    Returns:
        CSV bytes.
    """

    return df.to_csv(index=False).encode("utf-8")


def export_excel(df: pd.DataFrame) -> bytes:
    """
    Export DataFrame as Excel.

    Args:
        df: DataFrame to export.

    Returns:
        Excel file bytes.
    """

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Cleaned Data",
        )

    buffer.seek(0)

    return buffer.getvalue()


def export_report(report: dict) -> bytes:
    """
    Export analysis report as text.

    Args:
        report: Analysis dictionary.

    Returns:
        UTF-8 encoded report.
    """

    lines = []

    lines.append("=" * 60)
    lines.append("PREPWISE ANALYSIS REPORT")
    lines.append("=" * 60)
    lines.append("")

    for key, value in report.items():

        lines.append(f"{key.upper()}")

        lines.append("-" * 60)

        lines.append(str(value))

        lines.append("")

    return "\n".join(lines).encode("utf-8")


def save_file(
    data: bytes,
    output_path: str,
) -> None:
    """
    Save exported bytes to disk.

    Args:
        data: File bytes.
        output_path: Destination path.

    Raises:
        ExportError
    """

    extension = Path(output_path).suffix.lower()

    if extension not in SUPPORTED_EXPORTS and extension != ".txt":
        raise ExportError(
            f"Unsupported export format '{extension}'."
        )

    try:

        with open(output_path, "wb") as file:
            file.write(data)

    except Exception as exc:
        raise ExportError(
            f"Failed to save file: {exc}"
        ) from exc