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

    def process_data(self, filepath: str) -> pd.DataFrame:
        data = self.loader.load_data(filepath=filepath)
        data.columns = self.columns
        return data