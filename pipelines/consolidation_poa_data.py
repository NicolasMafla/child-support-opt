import os

import pandas as pd

from src.data import ExcelLoader
from src.utils import save_pandas_data, list_files

loader = ExcelLoader()
source_path = "./data/processed/poa"
final_path = "./data/processed/final"
filepaths = list_files(path=source_path)
filename = "poa"
ext = ".xlsx"

data_list = []
for filepath in filepaths:
    data = loader.load(filepath=filepath)
    data_list.append(data)

final = pd.concat(data_list)
output_filepath = os.path.join(final_path, f"{filename}{ext}")
save_pandas_data(input_data=final, filepath=output_filepath)