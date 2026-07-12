"""
frontend/analysis.py
"""

import streamlit as st

from backend.ai import AIService
from backend.analyzer import DatasetAnalyzer


class AnalysisPage:

    def __init__(self, dataframe):

        self.df = dataframe

        self.analyzer = DatasetAnalyzer(dataframe)

    def render(self):

        st.header("AI Analysis")

        report = self.analyzer.analyze()

        summary = report["summary"]

        st.subheader("Dataset Summary")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(

                "Quality Score",

                f"{report['quality_score']}%",

            )

            st.metric(

                "Rows",

                summary["rows"],

            )

            st.metric(

                "Columns",

                summary["columns"],

            )

        with col2:

            st.metric(

                "Missing Values",

                summary["missing_values"],

            )

            st.metric(

                "Duplicate Rows",

                summary["duplicate_rows"],

            )

            st.metric(

                "Memory (MB)",

                summary["memory_mb"],

            )

        st.divider()

        if st.button(

            "Generate AI Recommendations",

            type="primary",

            use_container_width=True,

        ):

            with st.spinner(

                "Analyzing your dataset and generating AI insights..."

            ):

                try:

                    ai = AIService()

                    result = ai.analyze_dataset(

                        report,

                    )

                    st.session_state["ai_report"] = result

                except Exception as e:

                    st.error(str(e))

        if st.session_state.get(

            "ai_report",

        ):

            st.divider()

            st.subheader(

                "AI Recommendations"

            )

            st.markdown(

                st.session_state["ai_report"]

            )

        with st.expander(

            "Feature Engineering Suggestions"

        ):

            if st.button(

                "Generate Suggestions",

                use_container_width=True,

            ):

                with st.spinner(

                    "Thinking..."

                ):

                    try:

                        ai = AIService()

                        suggestions = ai.feature_engineering(

                            list(self.df.columns)

                        )

                        st.markdown(

                            suggestions

                        )

                    except Exception as e:

                        st.error(

                            str(e)

                        )

        with st.expander(

            "Executive Summary"

        ):

            if st.button(

                "Generate Executive Summary",

                use_container_width=True,

            ):

                with st.spinner(

                    "Generating..."

                ):

                    try:

                        ai = AIService()

                        summary_text = ai.dashboard_summary(

                            report,

                        )

                        st.markdown(

                            summary_text

                        )

                    except Exception as e:

                        st.error(

                            str(e)

                        )