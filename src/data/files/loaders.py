import os
import pandas as pd
from src.data.files.models.loader import DataLoader


class ExcelLoader(DataLoader):
    def load(self, filepath: str, sheet_name: str = 0) -> pd.DataFrame:
        if os.path.exists(filepath):
            try:
                data = pd.read_excel(filepath, sheet_name=sheet_name)
                return data
            except Exception as e:
                print(f"{e}")
                return pd.DataFrame()
        else:
            print(f"Archivo no encontrado: {filepath}")
            return pd.DataFrame()


class CSVLoader(DataLoader):
    def load(self, filepath: str) -> pd.DataFrame:
        if os.path.exists(filepath):
            try:
                data = pd.read_csv(filepath)
                return data
            except Exception as e:
                print(f"{e}")
                return pd.DataFrame()
        else:
            print(f"Archivo no encontrado: {filepath}")
            return pd.DataFrame()
