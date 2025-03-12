from src.data import ExcelLoader, FCPDataProcessor

def test_fpc_load_data():
    excel_loader = ExcelLoader()
    processor = FCPDataProcessor(loader=excel_loader)
    data = processor.load_data(filepath="./data/raw/fcps.xlsx")
    assert len(data) > 1

def test_fcp_process_data():
    excel_loader = ExcelLoader()
    processor = FCPDataProcessor(loader=excel_loader)
    raw_data = processor.load_data(filepath="./data/raw/fcps.xlsx")
    processed_data = processor.process_data(input_data=raw_data)
    assert len(raw_data.columns) == len(processed_data.columns)
    assert len(raw_data) == len(processed_data)