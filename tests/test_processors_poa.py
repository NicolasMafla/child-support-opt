from src.data import CSVLoader, POADataProcessor

def test_fcp_process_data():
    loader = CSVLoader()
    processor = POADataProcessor(loader=loader)
    processed_data = processor.process(filepath="./data/test/EC0107.csv")
    assert len(processed_data) > 0