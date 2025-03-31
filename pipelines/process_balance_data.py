import os
import re
from src.data import ExcelLoader, BalanceDataProcessor
from src.utils import save_pandas_data, list_files, get_filename

loader = ExcelLoader()
source_path = "./data/raw/Balance de Comprobación FY24"
processed_path = "./data/processed/balance"
filepaths = list_files(path=source_path)
processor = BalanceDataProcessor(loader=loader)
ext = ".xlsx"

for filepath in filepaths:
    processed_data = processor.process(filepath=filepath)
    filename = get_filename(filepath=filepath)
    match = re.search(pattern="([A-Z]{2}\d{4})$", string=filename)
    fcp_id = match.group(1)
    output_filepath = os.path.join(processed_path, f"{fcp_id}{ext}")
    save_pandas_data(input_data=processed_data, filepath=output_filepath)