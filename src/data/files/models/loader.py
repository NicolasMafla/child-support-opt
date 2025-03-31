import pandas as pd
from typing import Dict
from abc import ABC, abstractmethod

class DataLoader(ABC):
    @abstractmethod
    def load(self, filepath: str) -> pd.DataFrame | Dict[str, pd.DataFrame]:
        pass