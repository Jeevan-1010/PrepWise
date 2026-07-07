import streamlit as st

from backend.loader import load_dataset
from backend.analyzer import (
    analyze_dataset,
    classify_columns,
    analyze_missing_values,
    detect_issues
)

st.set_page_config(
    page_title="PrepWise",
    page_icon="🍳",
    layout="wide"
)

st.title("PrepWise 🍳")
st.subheader("Let's uncook your cooked data.")

uploaded_file = st.file_uploader(
    "Upload your dataset",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Load dataset
    df = load_dataset(uploaded_file)

    # Backend Analysis
    summary = analyze_dataset(df)
    column_info = classify_columns(df)
    missing_df = analyze_missing_values(df)
    issues = detect_issues(df)

    # Dataset Preview
    st.write("## Dataset Preview")
    st.dataframe(df.head(), width="stretch")

    # Dataset Summary
    st.write("## Dataset Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Rows", summary["rows"])
        st.metric("Columns", summary["columns"])

    with col2:
        st.metric("Missing Values", summary["missing_values"])
        st.metric("Duplicate Rows", summary["duplicate_rows"])

    # Column Classification
    st.write("## Column Classification")
    st.dataframe(column_info, width="stretch")

    # Missing Value Analysis
    st.write("## Missing Value Analysis")
    st.dataframe(missing_df, width="stretch")

    # Issue Detection
    st.write("## 🚨 Issues Found")

    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("🎉 No major issues detected.")