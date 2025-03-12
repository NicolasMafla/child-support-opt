from src.data import CSVLoader, POADataProcessor

def test_fcp_process_data():
    loader = CSVLoader()
    processor = POADataProcessor(loader=loader)
    processed_data = processor.process_data(filepath="./data/raw/EC0107.csv")
    assert len(processed_data) > 0