"""
dashboard.py

Displays dataset statistics, previews and analysis.
"""

from typing import Dict

import pandas as pd
import streamlit as st


def render_overview(df: pd.DataFrame) -> None:
    """
    Display dataset overview metrics.
    """

    st.subheader("Dataset Overview")

    rows = len(df)
    columns = len(df.columns)
    missing = int(df.isnull().sum().sum())
    duplicates = int(df.duplicated().sum())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", f"{rows:,}")
    col2.metric("Columns", columns)
    col3.metric("Missing Values", missing)
    col4.metric("Duplicate Rows", duplicates)


def render_preview(df: pd.DataFrame) -> None:
    """
    Display dataset preview.
    """

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(),
        width="stretch",
        hide_index=True
    )


def render_data_types(df: pd.DataFrame) -> None:
    """
    Display column data types.
    """

    st.subheader("Column Data Types")

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(
        dtype_df,
        width="stretch",
        hide_index=True
    )


def render_missing_values(df: pd.DataFrame) -> None:
    """
    Display missing values analysis.
    """

    st.subheader("Missing Values")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Percentage": (
            (df.isnull().sum() / len(df)) * 100
        ).round(2).astype(str) + "%"
    })

    st.dataframe(
        missing_df,
        width="stretch",
        hide_index=True
    )


def render_numeric_summary(df: pd.DataFrame) -> None:
    """
    Display summary statistics.
    """

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return

    st.subheader("Summary Statistics")

    st.dataframe(
        numeric_df.describe().T,
        width="stretch"
    )


def render_analysis(results: Dict, df: pd.DataFrame) -> None:
    """
    Render the complete dashboard.
    """

    render_overview(df)

    st.divider()

    render_preview(df)

    st.divider()

    render_data_types(df)

    st.divider()

    render_missing_values(df)

    st.divider()

    render_numeric_summary(df)