# Configuration settings for VAS Dashboard

import os
from dotenv import load_dotenv

load_dotenv()

# Thresholds
LATENCY_THRESHOLD = int(os.getenv("LATENCY_THRESHOLD", 500))  # ms
ERROR_RATE_THRESHOLD = float(os.getenv("ERROR_RATE_THRESHOLD", 0.1))  # 10%

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'vas_logs'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'password')
}
