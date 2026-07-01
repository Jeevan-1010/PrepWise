import streamlit as st
import pandas as pd

from backend.loader import load_dataset
from backend.analyzer import analyze_dataset

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

    # Load dataset (Backend)
    df = load_dataset(uploaded_file)

    # Analyze dataset (Backend)
    summary = analyze_dataset(df)

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

    column_info = []

    for column in df.columns:
        dtype = str(df[column].dtype)

        if pd.api.types.is_numeric_dtype(df[column]):
            category = "Numerical 🔢"
        elif pd.api.types.is_datetime64_any_dtype(df[column]):
            category = "Datetime 📅"
        else:
            category = "Categorical 📝"

        column_info.append({
            "Column": column,
            "Data Type": dtype,
            "Category": category
        })

    st.dataframe(pd.DataFrame(column_info), width="stretch")

    # Missing Value Analysis
    st.write("## Missing Value Analysis")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Missing %": (df.isnull().sum() / len(df) * 100).round(2).values
    })

    st.dataframe(missing_df, width="stretch")

    # Issue Detection
    st.write("## 🚨 Issues Found")

    issues = []

    # Missing values
    for column in df.columns:
        missing = df[column].isnull().sum()

        if missing > 0:
            percent = (missing / len(df)) * 100
            issues.append(
                f"❌ '{column}' has {missing} missing values ({percent:.2f}%)."
            )

    # Duplicate rows
    duplicates = df.duplicated().sum()

    if duplicates > 0:
        issues.append(
            f"❌ Dataset contains {duplicates} duplicate rows."
        )

    # Identifier columns
    for column in df.columns:
        if df[column].nunique() == len(df):
            issues.append(
                f"⚠️ '{column}' looks like an identifier column."
            )

    # Display issues
    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("🎉 No major issues detected.")