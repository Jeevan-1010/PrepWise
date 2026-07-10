"""
frontend/dashboard.py
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from backend.analyzer import DatasetAnalyzer


class Dashboard:

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe

        self.analyzer = DatasetAnalyzer(dataframe)

    def render(self):

        st.header("Dataset Dashboard")

        summary = self.analyzer.basic_summary()

        quality = self.analyzer.quality_score()

        c1, c2, c3, c4, c5, c6 = st.columns(6)

        c1.metric("Rows", summary["rows"])

        c2.metric("Columns", summary["columns"])

        c3.metric("Missing", summary["missing_values"])

        c4.metric("Duplicates", summary["duplicate_rows"])

        c5.metric("Memory (MB)", summary["memory_mb"])

        c6.metric("Quality", f"{quality}%")

        st.divider()

        tab1, tab2, tab3, tab4, tab5 = st.tabs(

            [

                "Preview",

                "Missing",

                "Statistics",

                "Correlation",

                "Visualizations",

            ]

        )

        # --------------------------------------------------

        with tab1:

            st.subheader("Dataset Preview")

            st.dataframe(

                self.df,

                use_container_width=True,

            )

        # --------------------------------------------------

        with tab2:

            missing = self.analyzer.missing_values()

            st.dataframe(

                missing,

                use_container_width=True,

            )

        # --------------------------------------------------

        with tab3:

            stats = self.analyzer.summary_statistics()

            if stats.empty:

                st.info("No numeric columns found.")

            else:

                st.dataframe(

                    stats,

                    use_container_width=True,

                )

        # --------------------------------------------------

        with tab4:

            corr = self.analyzer.correlation_matrix()

            if corr.empty:

                st.info("Correlation matrix unavailable.")

            else:

                fig = px.imshow(

                    corr,

                    text_auto=".2f",

                    aspect="auto",

                    color_continuous_scale="RdBu",

                )

                fig.update_layout(

                    height=600,

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True,

                )

        # --------------------------------------------------

        with tab5:

            numeric = self.df.select_dtypes(

                include="number",

            )

            if numeric.empty:

                st.info("No numeric columns found.")

            else:

                column = st.selectbox(

                    "Select Numeric Column",

                    numeric.columns,

                )

                fig = px.histogram(

                    self.df,

                    x=column,

                    nbins=30,

                    title=f"Distribution of {column}",

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True,

                )

                if numeric.shape[1] >= 2:

                    x = st.selectbox(

                        "X Axis",

                        numeric.columns,

                        key="scatter_x",

                    )

                    y = st.selectbox(

                        "Y Axis",

                        numeric.columns,

                        index=1,

                        key="scatter_y",

                    )

                    scatter = px.scatter(

                        self.df,

                        x=x,

                        y=y,

                    )

                    st.plotly_chart(

                        scatter,

                        use_container_width=True,

                    )