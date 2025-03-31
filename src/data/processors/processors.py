import re
import pandas as pd
from typing import List, Dict
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
    def set_fcp_id(data: pd.DataFrame, fcp_id: str) -> pd.DataFrame:
        data["fcpId"] = fcp_id
        return data

    def process(self, filepath: str) -> pd.DataFrame:
        fcp_id = get_filename(filepath=filepath)
        data = self.loader.load(filepath=filepath)
        data = self.set_columns(data=data)
        data = self.remove_nans_by_col(data=data, col="account")
        data = self.parse_col_types(data=data)
        data = self.set_fcp_id(data=data, fcp_id=fcp_id)
        return data


class BalanceDataProcessor(DataProcessor):
    def __init__(self, loader: DataLoader):
        self.loader: DataLoader = loader
        self.columns: List[str] = ["account", "description", "before", "debe", "haber", "diff", "month"]

    def set_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        data.columns = self.columns
        return data

    def parse_data_sheets(self, info: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        data_list = []
        for i, (_, df) in enumerate(info.items(), 1):
            copy_df = df.copy()
            copy_df["month"] = f"m{i}"
            data_list.append(copy_df)
        data = pd.concat(data_list).reset_index(drop=True)
        data = data[data["Codigo"] != 204]
        return data

    @staticmethod
    def parse_col_types(data: pd.DataFrame) -> pd.DataFrame:
        data["account"] = data["account"].astype(int).astype(str)
        for col in ["before", "debe", "haber", "diff"]:
            data[col] = data[col].astype(float)
        return data

    @staticmethod
    def set_fcp_id(data: pd.DataFrame, fcp_id: str) -> pd.DataFrame:
        data["fcpId"] = fcp_id
        return data

    def process(self, filepath: str) -> pd.DataFrame:
        filename = get_filename(filepath=filepath)
        match = re.search(pattern="([A-Z]{2}\d{4})$", string=filename)
        fcp_id = match.group(1)

        info = self.loader.load(filepath=filepath, sheet_name=None, skiprows=5)
        data = self.parse_data_sheets(info=info)
        data = self.set_columns(data=data)
        data = self.parse_col_types(data=data)
        data = self.set_fcp_id(data=data, fcp_id=fcp_id)
        print(data)
        return data


