"""
cleaning.py

Provides the data cleaning interface for PrepWise.
"""

from typing import Optional

import pandas as pd
import streamlit as st

from backend.cleaner import (
    remove_duplicates,
    fill_missing_values,
    drop_missing_rows,
    drop_columns,
)


def render_cleaning_panel(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Render the data cleaning controls.

    Args:
        df: Input DataFrame.

    Returns:
        Cleaned DataFrame.
    """

    st.subheader("Data Cleaning")

    cleaned_df = df.copy()

    st.markdown("Choose the cleaning operations to apply.")

    st.divider()

    # --------------------------------------------------
    # Duplicate Removal
    # --------------------------------------------------

    remove_dup = st.checkbox(
        "Remove Duplicate Rows",
        value=False
    )

    if remove_dup:
        cleaned_df = remove_duplicates(cleaned_df)

    # --------------------------------------------------
    # Missing Values
    # --------------------------------------------------

    st.markdown("### Missing Value Handling")

    method = st.selectbox(
        "Choose a strategy",
        (
            "None",
            "Mean",
            "Median",
            "Mode",
            "Drop Rows"
        )
    )

    if method == "Mean":
        cleaned_df = fill_missing_values(
            cleaned_df,
            strategy="mean"
        )

    elif method == "Median":
        cleaned_df = fill_missing_values(
            cleaned_df,
            strategy="median"
        )

    elif method == "Mode":
        cleaned_df = fill_missing_values(
            cleaned_df,
            strategy="mode"
        )

    elif method == "Drop Rows":
        cleaned_df = drop_missing_rows(cleaned_df)

    st.divider()

    # --------------------------------------------------
    # Drop Columns
    # --------------------------------------------------

    selected_columns = st.multiselect(
        "Drop Columns",
        cleaned_df.columns.tolist()
    )

    if selected_columns:
        cleaned_df = drop_columns(
            cleaned_df,
            selected_columns
        )

    st.divider()

    st.success("Cleaning operations are ready.")

    return cleaned_df


def render_cleaned_preview(df: pd.DataFrame) -> None:
    """
    Display the cleaned dataset.
    """

    st.subheader("Cleaned Dataset Preview")

    st.dataframe(
        df.head(),
        width="stretch",
        hide_index=True
    )