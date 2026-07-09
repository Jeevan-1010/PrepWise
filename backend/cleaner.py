"""
backend.cleaner

Handles intelligent data cleaning and preprocessing.
"""

from __future__ import annotations

import pandas as pd
import numpy as np

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler,
    MinMaxScaler,
)


class DataCleaner:
    """
    Intelligent data cleaning engine.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    # --------------------------------------------------
    # Duplicate Handling
    # --------------------------------------------------

    def remove_duplicates(self) -> None:
        """Remove duplicate rows."""
        self.df.drop_duplicates(inplace=True)

    # --------------------------------------------------
    # Missing Values
    # --------------------------------------------------

    def fill_missing(
        self,
        strategy: str = "mean",
    ) -> None:
        """
        Fill missing values.

        Strategies:
        mean
        median
        mode
        """

        numeric = self.df.select_dtypes(include=np.number).columns

        categorical = self.df.select_dtypes(
            exclude=np.number
        ).columns

        if strategy == "mean":

            for col in numeric:
                self.df[col] = self.df[col].fillna(
                    self.df[col].mean()
                )

        elif strategy == "median":

            for col in numeric:
                self.df[col] = self.df[col].fillna(
                    self.df[col].median()
                )

        elif strategy == "mode":

            for col in self.df.columns:
                self.df[col] = self.df[col].fillna(
                    self.df[col].mode().iloc[0]
                )

        for col in categorical:

            self.df[col] = self.df[col].fillna(
                "Unknown"
            )

    # --------------------------------------------------
    # Drop Missing Rows
    # --------------------------------------------------

    def drop_missing_rows(self) -> None:
        """Drop rows containing missing values."""
        self.df.dropna(inplace=True)

    # --------------------------------------------------
    # Drop Columns
    # --------------------------------------------------

    def drop_columns(
        self,
        columns: list[str],
    ) -> None:

        self.df.drop(
            columns=columns,
            inplace=True,
            errors="ignore",
        )

    # --------------------------------------------------
    # Rename Columns
    # --------------------------------------------------

    def clean_column_names(self) -> None:

        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

    # --------------------------------------------------
    # Remove Constant Columns
    # --------------------------------------------------

    def remove_constant_columns(self) -> None:

        constant = [
            col
            for col in self.df.columns
            if self.df[col].nunique() <= 1
        ]

        self.df.drop(
            columns=constant,
            inplace=True,
        )

    # --------------------------------------------------
    # Encode Categories
    # --------------------------------------------------

    def label_encode(self) -> None:

        categorical = self.df.select_dtypes(
            include="object"
        ).columns

        encoder = LabelEncoder()

        for col in categorical:

            self.df[col] = encoder.fit_transform(
                self.df[col].astype(str)
            )

    # --------------------------------------------------
    # Scaling
    # --------------------------------------------------

    def standard_scale(self) -> None:

        numeric = self.df.select_dtypes(
            include=np.number
        ).columns

        scaler = StandardScaler()

        self.df[numeric] = scaler.fit_transform(
            self.df[numeric]
        )

    def minmax_scale(self) -> None:

        numeric = self.df.select_dtypes(
            include=np.number
        ).columns

        scaler = MinMaxScaler()

        self.df[numeric] = scaler.fit_transform(
            self.df[numeric]
        )

    # --------------------------------------------------
    # Outlier Removal
    # --------------------------------------------------

    def remove_outliers_iqr(self) -> None:

        numeric = self.df.select_dtypes(
            include=np.number
        )

        mask = pd.Series(
            True,
            index=self.df.index,
        )

        for column in numeric.columns:

            q1 = numeric[column].quantile(0.25)
            q3 = numeric[column].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            mask &= (
                (self.df[column] >= lower)
                &
                (self.df[column] <= upper)
            )

        self.df = self.df[mask]

    # --------------------------------------------------
    # Datetime Conversion
    # --------------------------------------------------

    def convert_datetime(self) -> None:

        for col in self.df.columns:

            try:
                converted = pd.to_datetime(
                    self.df[col],
                    errors="raise",
                )

                self.df[col] = converted

            except Exception:
                pass

    # --------------------------------------------------
    # Full Pipeline
    # --------------------------------------------------

    def clean(
        self,
        fill_strategy: str = "median",
    ) -> pd.DataFrame:
        """
        Execute complete cleaning pipeline.
        """

        self.clean_column_names()

        self.remove_duplicates()

        self.fill_missing(fill_strategy)

        self.remove_constant_columns()

        self.convert_datetime()

        return self.df