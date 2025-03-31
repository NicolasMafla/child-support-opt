import os
import pandas as pd
from typing import Dict
from config import logger
from src.data.files.models.loader import DataLoader


class ExcelLoader(DataLoader):
    def load(self, filepath: str, sheet_name: int = 0, skiprows=None) -> pd.DataFrame | Dict[str, pd.DataFrame]:
        if os.path.exists(filepath):
            try:
                data = pd.read_excel(filepath, sheet_name=sheet_name, skiprows=skiprows)
                logger.success(f"Successfully data loaded from {filepath}")
                return data
            except Exception as e:
                logger.error(f"Error loading {filepath} - {e}")
                return pd.DataFrame()
        else:
            logger.error(f"{filepath} not exist!")
            return pd.DataFrame()


class CSVLoader(DataLoader):
    def load(self, filepath: str) -> pd.DataFrame:
        if os.path.exists(filepath):
            try:
                data = pd.read_csv(filepath)
                logger.success(f"Successfully data loaded from {filepath}")
                return data
            except Exception as e:
                logger.error(f"Error loading {filepath} - {e}")
                return pd.DataFrame()
        else:
            logger.error(f"{filepath} not exist!")
            return pd.DataFrame()
