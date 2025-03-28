from src.data import ExcelLoader, FCPDataProcessor
from src.utils import save_pandas_data

loader = ExcelLoader()
raw_data_path = "./data/test/fcps.xlsx"
processed_data_path = "./data/processed/processed_fcps.xlsx"

processor = FCPDataProcessor(loader=loader)
processed_data = processor.process(filepath=raw_data_path)
save_pandas_data(input_data=processed_data, filepath=processed_data_path)
