from src import ExcelLoader

def test_excel_loader():
    excel_loader = ExcelLoader()
    excel_data = excel_loader.load_data(filepath="./data/raw/fcps.xlsx")
    assert len(excel_data) > 1