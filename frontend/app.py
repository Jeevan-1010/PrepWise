"""
frontend/app.py

PrepWise
Application Entry Point
"""

import sys
from pathlib import Path

import streamlit as st

# Add project root to Python path
ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui import PrepWiseUI

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(

    page_title="PrepWise",

    page_icon="",

    layout="wide",

    initial_sidebar_state="expanded",

)

# -------------------------------------------------------
# OPTIONAL CSS
# -------------------------------------------------------

css = Path("assets/styles.css")

if css.exists():

    st.markdown(

        f"<style>{css.read_text(encoding='utf-8')}</style>",

        unsafe_allow_html=True,

    )

# -------------------------------------------------------
# SESSION STATE
# -------------------------------------------------------

DEFAULTS = {

    "dataset": None,

    "cleaned_dataset": None,

    "analysis": None,

    "ai_report": None,

}

for key, value in DEFAULTS.items():

    st.session_state.setdefault(key, value)

# -------------------------------------------------------
# RUN APPLICATION
# -------------------------------------------------------

if __name__ == "__main__":

    PrepWiseUI().render()