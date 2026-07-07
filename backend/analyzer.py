import pandas as pd


def analyze_dataset(df):
    """Return basic dataset summary."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum())
    }


def classify_columns(df):
    """Classify dataset columns."""
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

    return pd.DataFrame(column_info)


def analyze_missing_values(df):
    """Return missing value analysis."""

    return pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Missing %": (
            df.isnull().sum() / len(df) * 100
        ).round(2).values
    })


def detect_issues(df):
    """Detect common dataset issues."""

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

    return issues