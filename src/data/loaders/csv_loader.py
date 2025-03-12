import os
import pandas as pd
from .loader import DataLoader

class CSVLoader(DataLoader):
    def load_data(self, filepath: str) -> pd.DataFrame:
        if os.path.exists(filepath):
            try:
                data = pd.read_csv(filepath)
                print(f"Datos cargados exitosamente desde {filepath}")
                return data
            except Exception as e:
                print(f"Error al cargar datos desde {filepath}: {e}")
                return pd.DataFrame()
        else:
            print(f"Archivo no encontrado: {filepath}")
            return pd.DataFrame()