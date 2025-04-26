import logging
import os

def setup_logger():
    logger = logging.getLogger('VAS_Dashboard')
    logger.setLevel(logging.INFO)
    
    os.makedirs('logs', exist_ok=True)
    fh = logging.FileHandler('logs/vas_dashboard.log')
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)

    return logger
