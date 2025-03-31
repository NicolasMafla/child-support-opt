import os
from src.data import ExcelLoader, FCPDataProcessor
from src.utils import save_pandas_data

loader = ExcelLoader()
raw_data_path = "./data/test/fcps.xlsx"
final_path = "./data/processed/final"
filename = "fcps"
ext = ".xlsx"

processor = FCPDataProcessor(loader=loader)
processed_data = processor.process(filepath=raw_data_path)
output_filepath = os.path.join(final_path, f"{filename}{ext}")
save_pandas_data(input_data=processed_data, filepath=output_filepath)
