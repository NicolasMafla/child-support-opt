import pandas as pd
from abc import ABC, abstractmethod

class DataLoader(ABC):
    @abstractmethod
    def load_data(self, filepath: str) -> pd.DataFrame:
        pass