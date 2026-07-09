"""
frontend.ui

Main UI controller for PrepWise.
"""

from __future__ import annotations

import streamlit as st

from frontend.sidebar import Sidebar
from frontend.dashboard import Dashboard
from frontend.cleaning import CleaningPage
from frontend.download import DownloadPage


class PrepWiseUI:
    """
    Main UI Controller.
    """

    def __init__(self):

        self.sidebar = Sidebar()

    def render(self):

        options = self.sidebar.render()

        uploaded_file = options["file"]

        if uploaded_file is None:

            st.title("PrepWise")

            st.markdown(
                """
# AI-Powered Data Preparation Platform

Welcome to **PrepWise**.

Upload a dataset from the sidebar to:

- Analyze your data
- Clean missing values
- Detect outliers
- Explore visualizations
- Generate AI insights
- Download the cleaned dataset
                """
            )

            return

        try:

            import pandas as pd

            if uploaded_file.name.endswith(".csv"):

                df = pd.read_csv(uploaded_file)

            else:

                df = pd.read_excel(uploaded_file)

        except Exception as exc:

            st.error(f"Unable to load dataset.\n\n{exc}")

            return

        # --------------------------------------------------
        # Dashboard
        # --------------------------------------------------

        dashboard = Dashboard(df)

        dashboard.render()

        st.divider()

        # --------------------------------------------------
        # Cleaning
        # --------------------------------------------------

        cleaning = CleaningPage(df)

        cleaned_df = cleaning.render()

        st.divider()

        # --------------------------------------------------
        # Download
        # --------------------------------------------------

        if cleaned_df is None:

            cleaned_df = df

        report = {
            "Rows": len(cleaned_df),
            "Columns": len(cleaned_df.columns),
            "Missing Values": int(cleaned_df.isna().sum().sum()),
            "Duplicate Rows": int(cleaned_df.duplicated().sum()),
        }

        download = DownloadPage(
            cleaned_df,
            report,
        )

        download.render()