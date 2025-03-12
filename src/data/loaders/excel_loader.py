import os
import pandas as pd
from .loader import DataLoader

class ExcelLoader(DataLoader):
    def load_data(self, filepath: str, sheet_name: str = 0) -> pd.DataFrame:
        """Carga datos desde un archivo Excel."""
        if os.path.exists(filepath):
            try:
                data = pd.read_excel(filepath, sheet_name=sheet_name)
                print(f"Datos cargados exitosamente desde {filepath}, hoja '{sheet_name}'")
                return data
            except Exception as e:
                print(f"Error al cargar datos desde {filepath}, hoja '{sheet_name}': {e}")
                return pd.DataFrame()
        else:
            print(f"Archivo no encontrado: {filepath}")
            return pd.DataFrame()