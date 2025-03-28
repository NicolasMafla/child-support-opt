import pandas as pd
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def process(self, filepath: str) -> pd.DataFrame:
        pass