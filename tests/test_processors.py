from src.data import ExcelLoader, CSVLoader, FCPDataProcessor, POADataProcessor, BalanceDataProcessor

def test_fcp_process_data():
    excel_loader = ExcelLoader()
    processor = FCPDataProcessor(loader=excel_loader)
    processed_data = processor.process(filepath="./data/test/fcps.xlsx")
    assert len(processed_data) > 0

def test_poa_process_data():
    loader = CSVLoader()
    processor = POADataProcessor(loader=loader)
    processed_data = processor.process(filepath="./data/test/EC0107.csv")
    assert len(processed_data) > 0


def test_balance_process_data():
    loader = ExcelLoader()
    processor = BalanceDataProcessor(loader=loader)
    processed_data = processor.process(filepath="./data/test/Balance_de_Comprobacion_EC0133.xlsx")
    assert len(processed_data) > 0