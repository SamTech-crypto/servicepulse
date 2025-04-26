import pandas as pd
from logger import setup_logger  

def load_data(file_path):
    """
    Load VAS logs from CSV file.
    """
    logger = setup_logger()
    try:
        logger.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['status'] = df['status'].str.lower()  # Normalize status
        return df
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise
