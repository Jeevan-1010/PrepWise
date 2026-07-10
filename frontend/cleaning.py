"""
frontend/cleaning.py
"""

import pandas as pd
import streamlit as st

from backend.cleaner import DataCleaner


class CleaningPage:

    def __init__(self, dataframe: pd.DataFrame):

        self.original = dataframe

    def render(self):

        st.header("Data Cleaning")

        st.write(
            "Configure preprocessing operations and clean your dataset."
        )

        left, right = st.columns(2)

        with left:

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

        with right:

            encode = st.checkbox(

                "Label Encode Categorical Columns",

                value=False,

            )

            scaling = st.selectbox(

                "Scaling",

                [

                    "None",

                    "Standard",

                    "MinMax",

                ],

            )

        st.divider()

        if st.button(

            "Start Cleaning",

            type="primary",

            use_container_width=True,

        ):

            cleaner = DataCleaner(self.original)

            cleaner.clean_column_names()

            if remove_duplicates:

                cleaner.remove_duplicates()

            cleaner.fill_missing(fill_strategy)

            if remove_outliers:

                cleaner.remove_outliers_iqr()

            if encode:

                cleaner.label_encode()

            if scaling == "Standard":

                cleaner.standard_scale()

            elif scaling == "MinMax":

                cleaner.minmax_scale()

            cleaned = cleaner.df

            st.session_state["cleaned_dataset"] = cleaned

            st.success("Dataset cleaned successfully.")

        cleaned = st.session_state.get(

            "cleaned_dataset",

            self.original,

        )

        st.divider()

        c1, c2 = st.columns(2)

        c1.metric(

            "Rows",

            len(cleaned),

        )

        c2.metric(

            "Columns",

            len(cleaned.columns),

        )

        st.subheader("Cleaned Dataset Preview")

        st.dataframe(

            cleaned,

            use_container_width=True,

            height=450,

        )

        return cleaned