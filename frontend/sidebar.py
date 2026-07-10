"""
frontend/sidebar.py
"""

import streamlit as st


class Sidebar:

    def render(self):

        with st.sidebar:

            st.title("PrepWise")

            st.caption(
                "AI Powered Data Preparation Platform"
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

            st.subheader("Cleaning")

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

                "Label Encode",

                value=False,

            )

            scaling = st.selectbox(

                "Scaling",

                [

                    "None",

                    "Standard",

                    "MinMax",

                ],

            )

            st.divider()

            st.subheader("AI")

            generate_ai = st.button(

                "Generate AI Report",

                use_container_width=True,

            )

            st.divider()

            clean_data = st.button(

                "Clean Dataset",

                type="primary",

                use_container_width=True,

            )

            return {

                "uploaded_file": uploaded_file,

                "fill_strategy": fill_strategy,

                "remove_duplicates": remove_duplicates,

                "remove_outliers": remove_outliers,

                "encode": encode,

                "scaling": scaling,

                "clean_data": clean_data,

                "generate_ai": generate_ai,

            }