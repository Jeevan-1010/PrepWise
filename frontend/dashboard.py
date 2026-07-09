"""
frontend.dashboard

Main dashboard for PrepWise.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


class Dashboard:

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe

    # --------------------------------------------------
    # KPI Cards
    # --------------------------------------------------

    def render_metrics(self):

        rows = len(self.df)

        cols = len(self.df.columns)

        missing = int(self.df.isna().sum().sum())

        duplicates = int(self.df.duplicated().sum())

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Rows",
            f"{rows:,}",
        )

        c2.metric(
            "Columns",
            cols,
        )

        c3.metric(
            "Missing Values",
            missing,
        )

        c4.metric(
            "Duplicate Rows",
            duplicates,
        )

    # --------------------------------------------------
    # Dataset Preview
    # --------------------------------------------------

    def render_preview(self):

        st.subheader("Dataset Preview")

        st.dataframe(
            self.df,
            use_container_width=True,
            height=400,
        )

    # --------------------------------------------------
    # Missing Values
    # --------------------------------------------------

    def render_missing_chart(self):

        missing = (
            self.df.isna()
            .sum()
            .reset_index()
        )

        missing.columns = [
            "Column",
            "Missing",
        ]

        fig = px.bar(
            missing,
            x="Column",
            y="Missing",
            title="Missing Values",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # --------------------------------------------------
    # Correlation
    # --------------------------------------------------

    def render_correlation(self):

        numeric = self.df.select_dtypes(
            include="number",
        )

        if numeric.shape[1] < 2:
            return

        corr = numeric.corr()

        fig = px.imshow(
            corr,
            text_auto=".2f",
            title="Correlation Matrix",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # --------------------------------------------------
    # Distributions
    # --------------------------------------------------

    def render_distributions(self):

        numeric = self.df.select_dtypes(
            include="number",
        ).columns

        if len(numeric) == 0:
            return

        column = st.selectbox(
            "Distribution",
            numeric,
        )

        fig = px.histogram(
            self.df,
            x=column,
            nbins=40,
            title=f"{column} Distribution",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # --------------------------------------------------
    # Scatter Plot
    # --------------------------------------------------

    def render_scatter(self):

        numeric = self.df.select_dtypes(
            include="number",
        ).columns.tolist()

        if len(numeric) < 2:
            return

        c1, c2 = st.columns(2)

        x = c1.selectbox(
            "X Axis",
            numeric,
            key="scatter_x",
        )

        y = c2.selectbox(
            "Y Axis",
            numeric,
            index=1,
            key="scatter_y",
        )

        fig = px.scatter(
            self.df,
            x=x,
            y=y,
            title=f"{x} vs {y}",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # --------------------------------------------------
    # Data Types
    # --------------------------------------------------

    def render_datatypes(self):

        st.subheader("Column Types")

        dtype = pd.DataFrame(
            {
                "Column": self.df.columns,
                "Data Type": self.df.dtypes.astype(str),
            }
        )

        st.dataframe(
            dtype,
            use_container_width=True,
        )

    # --------------------------------------------------
    # Dashboard
    # --------------------------------------------------

    def render(self):

        st.title("PrepWise Dashboard")

        self.render_metrics()

        st.divider()

        self.render_preview()

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            self.render_missing_chart()

        with c2:
            self.render_correlation()

        st.divider()

        c3, c4 = st.columns(2)

        with c3:
            self.render_distributions()

        with c4:
            self.render_scatter()

        st.divider()

        self.render_datatypes()