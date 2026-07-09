"""
frontend.download

Download page for PrepWise.
"""

from __future__ import annotations

import streamlit as st

from backend.exporter import (
    export_csv,
    export_excel,
    export_report,
)


class DownloadPage:

    def __init__(
        self,
        dataframe,
        report=None,
    ):
        self.df = dataframe
        self.report = report

    def render(self):

        st.title("Export")

        st.write(
            "Download your cleaned dataset and analysis reports."
        )

        st.divider()

        csv_data = export_csv(self.df)

        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="prepwise_cleaned.csv",
            mime="text/csv",
            use_container_width=True,
        )

        excel_data = export_excel(self.df)

        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name="prepwise_cleaned.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

        if self.report is not None:

            report_data = export_report(self.report)

            st.download_button(
                label="Download Analysis Report",
                data=report_data,
                file_name="prepwise_report.txt",
                mime="text/plain",
                use_container_width=True,
            )

        st.success("Your files are ready for download.")