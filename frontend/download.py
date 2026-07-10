"""
frontend/download.py
"""

import streamlit as st

from backend.exporter import (
    export_csv,
    export_excel,
    export_report,
)


class DownloadPage:

    def __init__(self, dataframe, analysis=None):

        self.df = dataframe

        self.analysis = analysis

    def render(self):

        st.header("Download Center")

        st.write(
            "Export the processed dataset and analysis report."
        )

        st.divider()

        csv_data = export_csv(

            self.df,

        )

        excel_data = export_excel(

            self.df,

        )

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(

                label="Download CSV",

                data=csv_data,

                file_name="prepwise_cleaned_dataset.csv",

                mime="text/csv",

                use_container_width=True,

            )

        with col2:

            st.download_button(

                label="Download Excel",

                data=excel_data,

                file_name="prepwise_cleaned_dataset.xlsx",

                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                use_container_width=True,

            )

        st.divider()

        if self.analysis is not None:

            report = export_report(

                self.analysis,

            )

            st.download_button(

                label="Download Analysis Report",

                data=report,

                file_name="prepwise_analysis_report.txt",

                mime="text/plain",

                use_container_width=True,

            )

        if st.session_state.get(

            "ai_report",

        ):

            st.download_button(

                label="Download AI Report",

                data=st.session_state["ai_report"],

                file_name="prepwise_ai_report.md",

                mime="text/markdown",

                use_container_width=True,

            )