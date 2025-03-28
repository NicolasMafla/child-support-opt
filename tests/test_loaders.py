from src.data import ExcelLoader, CSVLoader

def test_excel_loader():
    loader = ExcelLoader()
    data = loader.load(filepath="./data/test/fcps.xlsx")
    assert len(data) > 1

def test_csv_loader():
    loader = CSVLoader()
    data = loader.load(filepath="./data/test/EC0107.csv")
    assert len(data) > 1