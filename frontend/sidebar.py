"""
frontend.sidebar

Sidebar component for PrepWise.
"""

from __future__ import annotations

import streamlit as st


class Sidebar:

    def __init__(self):
        pass

    def render(self):

        with st.sidebar:

            st.markdown(
                """
                # PrepWise

                **AI-Powered Data Preparation Platform**
                """
            )

            st.divider()

            uploaded_file = st.file_uploader(
                "Upload Dataset",
                type=[
                    "csv",
                    "xlsx",
                ],
            )

            st.divider()

            st.subheader("Cleaning Options")

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
                "Remove Outliers",
                value=True,
            )

            encode = st.checkbox(
                "Encode Categorical Columns",
                value=False,
            )

            standardize = st.checkbox(
                "Standard Scale",
                value=False,
            )

            st.divider()

            st.subheader("Machine Learning")

            run_clustering = st.checkbox(
                "KMeans Clustering",
                value=True,
            )

            run_outlier_detection = st.checkbox(
                "Isolation Forest",
                value=True,
            )

            run_pca = st.checkbox(
                "PCA Projection",
                value=True,
            )

            st.divider()

            analyze = st.button(
                "Analyze Dataset",
                use_container_width=True,
            )

            clean = st.button(
                "Clean Dataset",
                use_container_width=True,
            )

            ai = st.button(
                "AI Recommendations",
                use_container_width=True,
            )

            return {
                "file": uploaded_file,
                "fill_strategy": fill_strategy,
                "remove_duplicates": remove_duplicates,
                "remove_outliers": remove_outliers,
                "encode": encode,
                "standardize": standardize,
                "run_clustering": run_clustering,
                "run_outlier_detection": run_outlier_detection,
                "run_pca": run_pca,
                "analyze": analyze,
                "clean": clean,
                "ai": ai,
            }