import io
import pandas as pd


def export_csv(df):
    """
    Export DataFrame as CSV bytes.
    """

    csv_data = df.to_csv(index=False)

    return csv_data.encode("utf-8")


def export_excel(df):
    """
    Export DataFrame as Excel bytes.
    """

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Cleaned Dataset")

    output.seek(0)

    return output.getvalue()


def get_file_size(data):
    """
    Return exported file size in bytes.
    """

    return len(data)