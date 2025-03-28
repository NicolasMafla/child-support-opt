import pandas as pd
from typing import List
from ..files import DataLoader
from .models.processor import DataProcessor
from ...utils import get_filename, money_to_float


class FCPDataProcessor(DataProcessor):
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

    def process(self, filepath: str) -> pd.DataFrame:
        data = self.loader.load(filepath=filepath)
        data.columns = self.columns
        return data


class POADataProcessor(DataProcessor):
    def __init__(self, loader: DataLoader):
        self.loader: DataLoader = loader
        self.columns: List[str] = ["activity", "group", "account", "total"] + [f"m{i}" for i in range(1, 13)]

    def set_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        data.columns = self.columns
        return data

    @staticmethod
    def remove_nans_by_col(data: pd.DataFrame, col: str) -> pd.DataFrame:
        data = data[data[col].notnull()]
        return data

    @staticmethod
    def parse_col_types(data: pd.DataFrame) -> pd.DataFrame:
        data["account"] = data["account"].astype(int).astype(str)
        data["total"] = data["total"].apply(money_to_float)
        for col in [f"m{i}" for i in range(1, 13)]:
            if data[col].dtype.name == "object":
                data[col] = data[col].apply(money_to_float)
            else:
                data[col] = data[col].astype(float)
        return data

    @staticmethod
    def set_poa_id(data: pd.DataFrame, poa_id: str) -> pd.DataFrame:
        data["fcpId"] = poa_id
        return data

    def process(self, filepath: str) -> pd.DataFrame:
        poa_id = get_filename(filepath=filepath)
        data = self.loader.load(filepath=filepath)
        data = self.set_columns(data=data)
        data = self.remove_nans_by_col(data=data, col="account")
        data = self.parse_col_types(data=data)
        data = self.set_poa_id(data=data, poa_id=poa_id)
        return data
