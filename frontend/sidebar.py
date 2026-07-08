"""
sidebar.py

Handles all Streamlit sidebar components.
"""

from typing import Optional

import streamlit as st


def render_sidebar() -> Optional[object]:
    """
    Render the application sidebar.

    Returns:
        Uploaded file object if a file is selected,
        otherwise None.
    """

    with st.sidebar:

        st.title("PrepWise")

        st.caption("AI-Powered Data Cleaning Assistant")

        st.divider()

        uploaded_file = st.file_uploader(
            "Upload Dataset",
            type=["csv", "xlsx"],
            help="Supported formats: CSV and Excel (.xlsx)"
        )

        st.divider()

        st.subheader("Supported Files")

        st.markdown(
            """
            - CSV (.csv)
            - Excel (.xlsx)
            """
        )

        st.divider()

        st.subheader("Workflow")

        st.markdown(
            """
            1. Upload Dataset
            2. Analyze Dataset
            3. Clean Data
            4. Download Clean Dataset
            """
        )

        st.divider()

        st.caption("PrepWise v1.0")

    return uploaded_file


def show_dataset_info(df) -> None:
    """
    Display dataset information in the sidebar.

    Args:
        df: Loaded pandas DataFrame.
    """

    with st.sidebar:

        st.divider()

        st.subheader("Dataset Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Rows", len(df))

        with col2:
            st.metric("Columns", len(df.columns))

        memory = df.memory_usage(deep=True).sum() / (1024 ** 2)

        st.metric(
            "Memory Usage",
            f"{memory:.2f} MB"
        )