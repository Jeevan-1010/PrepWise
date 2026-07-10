"""
frontend/ui.py
"""

import pandas as pd
import streamlit as st

from sidebar import Sidebar
from dashboard import Dashboard
from cleaning import CleaningPage
from analysis import AnalysisPage
from download import DownloadPage

from backend.analyzer import DatasetAnalyzer


class PrepWiseUI:

    def __init__(self):

        self.sidebar = Sidebar()

    def load_dataset(self, uploaded_file):

        if uploaded_file.name.lower().endswith(".csv"):

            return pd.read_csv(uploaded_file)

        elif uploaded_file.name.lower().endswith(".xlsx"):

            return pd.read_excel(uploaded_file)

        return None

    def render(self):

        options = self.sidebar.render()

        uploaded_file = options["uploaded_file"]

        st.title("PrepWise")

        st.caption(
            "AI Powered Data Preparation Platform"
        )

        st.divider()

        if uploaded_file is None:

            st.info(
                "Upload a CSV or Excel dataset from the sidebar."
            )

            return

        if (

            st.session_state["dataset"] is None

            or

            uploaded_file.name != st.session_state.get(
                "dataset_name"
            )

        ):

            df = self.load_dataset(uploaded_file)

            st.session_state["dataset"] = df

            st.session_state["dataset_name"] = uploaded_file.name

            st.session_state["cleaned_dataset"] = df.copy()

            st.session_state["analysis"] = None

            st.session_state["ai_report"] = None

        original_df = st.session_state["dataset"]

        cleaned_df = st.session_state["cleaned_dataset"]

        # ----------------------------------------------------
        # DATASET OVERVIEW
        # ----------------------------------------------------

        Dashboard(cleaned_df).render()

        st.divider()

        # ----------------------------------------------------
        # CLEANING
        # ----------------------------------------------------

        cleaned_df = CleaningPage(

            cleaned_df,

        ).render()

        st.session_state["cleaned_dataset"] = cleaned_df

        st.divider()

        # ----------------------------------------------------
        # ANALYSIS
        # ----------------------------------------------------

        analyzer = DatasetAnalyzer(

            cleaned_df,

        )

        analysis = analyzer.analyze()

        st.session_state["analysis"] = analysis

        AnalysisPage(

            cleaned_df,

        ).render()

        st.divider()

        # ----------------------------------------------------
        # DOWNLOADS
        # ----------------------------------------------------

        DownloadPage(

            cleaned_df,

            analysis,

        ).render()