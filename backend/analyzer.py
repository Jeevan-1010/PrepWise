"""
backend.analyzer

Performs dataset profiling and machine learning analysis.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest


class DatasetAnalyzer:
    """
    Performs exploratory analysis and ML-based dataset inspection.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    # ----------------------------------------------------
    # Basic Information
    # ----------------------------------------------------

    def basic_summary(self) -> dict:
        return {
            "rows": len(self.df),
            "columns": len(self.df.columns),
            "missing_values": int(self.df.isna().sum().sum()),
            "duplicate_rows": int(self.df.duplicated().sum()),
            "memory_mb": round(
                self.df.memory_usage(deep=True).sum() / (1024 ** 2),
                2,
            ),
        }

    # ----------------------------------------------------
    # Missing Values
    # ----------------------------------------------------

    def missing_values(self) -> pd.DataFrame:

        missing = self.df.isnull().sum()

        return pd.DataFrame(
            {
                "Column": missing.index,
                "Missing Values": missing.values,
                "Percentage": (
                    missing / len(self.df) * 100
                ).round(2),
            }
        )

    # ----------------------------------------------------
    # Data Types
    # ----------------------------------------------------

    def data_types(self) -> pd.DataFrame:

        return pd.DataFrame(
            {
                "Column": self.df.columns,
                "Data Type": self.df.dtypes.astype(str),
            }
        )

    # ----------------------------------------------------
    # Summary Statistics
    # ----------------------------------------------------

    def summary_statistics(self) -> pd.DataFrame:

        numeric = self.df.select_dtypes(include=np.number)

        if numeric.empty:
            return pd.DataFrame()

        return numeric.describe().T

    # ----------------------------------------------------
    # Correlation Matrix
    # ----------------------------------------------------

    def correlation_matrix(self) -> pd.DataFrame:

        numeric = self.df.select_dtypes(include=np.number)

        if numeric.shape[1] < 2:
            return pd.DataFrame()

        return numeric.corr()

    # ----------------------------------------------------
    # Quality Score
    # ----------------------------------------------------

    def quality_score(self) -> float:

        score = 100

        score -= self.df.isnull().sum().sum() * 0.2

        score -= self.df.duplicated().sum() * 2

        constant_columns = (
            self.df.nunique() <= 1
        ).sum()

        score -= constant_columns * 5

        return round(max(score, 0), 2)

    # ----------------------------------------------------
    # Isolation Forest
    # ----------------------------------------------------

    def detect_outliers(self) -> pd.Series:

        numeric = self.df.select_dtypes(include=np.number)

        if numeric.shape[1] == 0:
            return pd.Series(dtype=int)

        clean = numeric.fillna(numeric.mean())

        model = IsolationForest(
            contamination=0.05,
            random_state=42,
        )

        return pd.Series(
            model.fit_predict(clean),
            index=self.df.index,
        )

    # ----------------------------------------------------
    # KMeans Clustering
    # ----------------------------------------------------

    def cluster_data(
        self,
        n_clusters: int = 3,
    ) -> pd.Series:

        numeric = self.df.select_dtypes(include=np.number)

        if numeric.shape[1] == 0:
            return pd.Series(dtype=int)

        clean = numeric.fillna(numeric.mean())

        model = KMeans(
            n_clusters=n_clusters,
            random_state=42,
            n_init="auto",
        )

        labels = model.fit_predict(clean)

        return pd.Series(
            labels,
            index=self.df.index,
        )

    # ----------------------------------------------------
    # PCA
    # ----------------------------------------------------

    def pca_projection(
        self,
        components: int = 2,
    ) -> pd.DataFrame:

        numeric = self.df.select_dtypes(include=np.number)

        if numeric.shape[1] < components:
            return pd.DataFrame()

        clean = numeric.fillna(numeric.mean())

        pca = PCA(
            n_components=components,
            random_state=42,
        )

        transformed = pca.fit_transform(clean)

        columns = [
            f"PC{i+1}"
            for i in range(components)
        ]

        return pd.DataFrame(
            transformed,
            columns=columns,
        )

    # ----------------------------------------------------
    # Complete Analysis
    # ----------------------------------------------------

    def analyze(self) -> dict:

        return {
            "summary": self.basic_summary(),
            "missing_values": self.missing_values(),
            "data_types": self.data_types(),
            "statistics": self.summary_statistics(),
            "correlation": self.correlation_matrix(),
            "quality_score": self.quality_score(),
            "outliers": self.detect_outliers(),
            "clusters": self.cluster_data(),
            "pca": self.pca_projection(),
        }