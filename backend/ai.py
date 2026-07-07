import pandas as pd


def build_dataset_summary(df):
    """
    Build a concise summary of the dataset
    to send to the AI model.
    """

    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_types": {}
    }

    for column in df.columns:
        summary["column_types"][column] = str(df[column].dtype)

    return summary


def build_prompt(df):
    """
    Build a prompt for the AI model.
    """

    summary = build_dataset_summary(df)

    prompt = f"""
You are an expert data scientist.

Analyze the following dataset summary and provide recommendations.

Dataset Summary
---------------
Rows: {summary['rows']}
Columns: {summary['columns']}
Missing Values: {summary['missing_values']}
Duplicate Rows: {summary['duplicate_rows']}

Column Types:
"""

    for column, dtype in summary["column_types"].items():
        prompt += f"\n- {column}: {dtype}"

    prompt += """

Please provide:

1. Dataset quality score (0-100)
2. Major issues found
3. Recommended cleaning steps
4. Feature engineering suggestions
5. Machine Learning readiness
"""

    return prompt


def get_ai_recommendation(df):
    """
    Placeholder until Gemini integration.
    """

    return {
        "status": "Not Connected",
        "message": (
            "AI integration will be enabled after "
            "connecting Gemini API."
        ),
        "prompt": build_prompt(df)
    }