import pandas as pd


def remove_duplicates(df):
    """Remove duplicate rows."""
    return df.drop_duplicates()


def drop_missing_rows(df):
    """Remove rows containing missing values."""
    return df.dropna()


def fill_missing_mean(df):
    """Fill numeric missing values with mean."""

    df = df.copy()

    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].mean())

    return df


def fill_missing_median(df):
    """Fill numeric missing values with median."""

    df = df.copy()

    numeric_columns = df.select_dtypes(include="number").columns

    for column in numeric_columns:
        df[column] = df[column].fillna(df[column].median())

    return df


def fill_missing_mode(df):
    """Fill missing values using mode."""

    df = df.copy()

    for column in df.columns:

        mode = df[column].mode()

        if not mode.empty:
            df[column] = df[column].fillna(mode.iloc[0])

    return df


def drop_columns(df, columns):
    """Drop selected columns."""

    return df.drop(columns=columns)


def rename_column(df, old_name, new_name):
    """Rename a column."""

    return df.rename(columns={
        old_name: new_name
    })


def convert_dtype(df, column, dtype):
    """Convert column datatype."""

    df = df.copy()

    df[column] = df[column].astype(dtype)

    return df