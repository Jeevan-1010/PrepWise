"""
frontend.cleaning

Cleaning page for PrepWise.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from backend.cleaner import DataCleaner


class CleaningPage:

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    def render(self):

        st.title("Data Cleaning")

        st.write(
            "Configure how PrepWise should clean your dataset."
        )

        st.divider()

        fill_strategy = st.selectbox(
            "Missing Value Strategy",
            [
                "mean",
                "median",
                "mode",
            ],
        )

        remove_duplicates = st.checkbox(
            "Remove Duplicate Rows",
            value=True,
        )

        remove_outliers = st.checkbox(
            "Remove Outliers (IQR)",
            value=True,
        )

        encode = st.checkbox(
            "Label Encode Categorical Columns"
        )

        scale = st.selectbox(
            "Scaling",
            [
                "None",
                "Standard",
                "MinMax",
            ],
        )

        if st.button(
            "Start Cleaning",
            use_container_width=True,
        ):

            cleaner = DataCleaner(self.df)

            cleaner.clean_column_names()

            if remove_duplicates:
                cleaner.remove_duplicates()

            cleaner.fill_missing(fill_strategy)

            cleaner.remove_constant_columns()

            cleaner.convert_datetime()

            if remove_outliers:
                cleaner.remove_outliers_iqr()

            if encode:
                cleaner.label_encode()

            if scale == "Standard":
                cleaner.standard_scale()

            elif scale == "MinMax":
                cleaner.minmax_scale()

            cleaned = cleaner.df

            st.success("Dataset cleaned successfully.")

            st.subheader("Preview")

            st.dataframe(
                cleaned,
                use_container_width=True,
            )

            st.session_state["cleaned_df"] = cleaned

            return cleaned

        return None