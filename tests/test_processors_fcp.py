from src.data import ExcelLoader, FCPDataProcessor

def test_fcp_process_data():
    excel_loader = ExcelLoader()
    processor = FCPDataProcessor(loader=excel_loader)
    processed_data = processor.process_data(filepath="./data/raw/fcps.xlsx")
    assert len(processed_data) > 0