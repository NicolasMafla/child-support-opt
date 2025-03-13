import os
from src.data import CSVLoader, POADataProcessor
from src.utils import save_pandas_data, list_files, get_filename

loader = CSVLoader()
source_path = "./data/raw/POA FY24"
processed_path = "./data/processed/poa"
filepaths = list_files(path=source_path)
processor = POADataProcessor(loader=loader)
ext = ".xlsx"

for filepath in filepaths:
    processed_data = processor.process_data(filepath=filepath)
    filename = get_filename(filepath=filepath)
    output_filepath = os.path.join(processed_path, f"{filename}{ext}")
    save_pandas_data(input_data=processed_data, filepath=output_filepath)
    print(f"Processed: {filepath}")