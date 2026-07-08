"""
download.py

Handles dataset export functionality.
"""

import pandas as pd
import streamlit as st

from backend.exporter import export_csv, export_excel


def render_download_section(df: pd.DataFrame) -> None:
    """
    Render download buttons for the cleaned dataset.

    Args:
        df: Cleaned pandas DataFrame.
    """

    st.subheader("Download Cleaned Dataset")

    st.markdown(
        "Choose a format to download your cleaned dataset."
    )

    csv_data = export_csv(df)
    excel_data = export_excel(df)

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="cleaned_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:

        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name="cleaned_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    st.success("Your cleaned dataset is ready for download.")