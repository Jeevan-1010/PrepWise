"""
frontend.app

Entry point for the PrepWise Streamlit application.
"""

from __future__ import annotations

import streamlit as st

from frontend.ui import PrepWiseUI


def configure_page() -> None:
    """
    Configure Streamlit page settings.
    """

    st.set_page_config(
        page_title="PrepWise",
        page_icon="assets/favicon.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def load_css() -> None:
    """
    Load custom CSS.
    """

    try:
        with open("assets/styles.css", "r", encoding="utf-8") as css:
            st.markdown(
                f"<style>{css.read()}</style>",
                unsafe_allow_html=True,
            )
    except FileNotFoundError:
        pass


def initialize_session() -> None:

    defaults = {
        "cleaned_df": None,
        "analysis": None,
        "report": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main() -> None:

    configure_page()

    load_css()

    initialize_session()

    ui = PrepWiseUI()

    ui.render()


if __name__ == "__main__":
    main()