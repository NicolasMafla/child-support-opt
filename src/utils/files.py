import os
import pandas as pd

def save_pandas_data(input_data: pd.DataFrame, filepath: str) -> None:
    if filepath.endswith(".csv"):
        input_data.to_csv(filepath, index=False)
    elif filepath.endswith(".xlsx"):
        input_data.to_excel(filepath, index=False)
    else:
        raise ValueError("El archivo debe tener extensión .csv o .xlsx")

def file_exists(path: str) -> bool:
    return os.path.isfile(path)


def get_filename(filepath: str) -> str:
    filename_ext = os.path.basename(filepath)
    filename = os.path.splitext(filename_ext)[0]
    return filename