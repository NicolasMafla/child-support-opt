import pandas as pd
from typing import List
from ..loaders import DataLoader

class FCPDataProcessor:
    def __init__(self, loader: DataLoader):
        self.loader: DataLoader = loader
        self.columns: List[str] = [
            "fcpId",
            "fpcStatus",
            "fcpType",
            "fpcCurrentParticipants",
            "fcpSponsoredParticipants",
            "fcpUnsponsoredParticipants",
            "fpcSurvivalParticipants",
            "fpcAllocatedSurvivalSlots",
            "fcpCity",
            "fcpState",
            "fcpLat",
            "fcpLon"
        ]

    def load_data(self, filepath: str) -> pd.DataFrame:
        return self.loader.load_data(filepath=filepath)

    def process_data(self, input_data: pd.DataFrame) -> pd.DataFrame:
        data = input_data.copy()
        data.columns = self.columns
        return data