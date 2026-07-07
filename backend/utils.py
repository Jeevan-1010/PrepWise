import pandas as pd


def format_bytes(size):
    """
    Convert bytes into a human-readable format.
    """

    for unit in ["B", "KB", "MB", "GB", "TB"]:

        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def format_percentage(value, total):
    """
    Calculate percentage safely.
    """

    if total == 0:
        return 0

    return round((value / total) * 100, 2)


def infer_column_type(series):
    """
    Infer a user-friendly column type.
    """

    if pd.api.types.is_numeric_dtype(series):
        return "Numerical"

    elif pd.api.types.is_datetime64_any_dtype(series):
        return "Datetime"

    elif pd.api.types.is_bool_dtype(series):
        return "Boolean"

    else:
        return "Categorical"


def validate_dataset(df):
    """
    Validate uploaded dataset.
    """

    if df.empty:
        return False, "Dataset is empty."

    if len(df.columns) == 0:
        return False, "Dataset has no columns."

    return True, "Dataset is valid."