"""
Application Configuration

Centralized configuration values.
Keeps constants separated from business logic.
"""

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

# ML configuration
ROLLING_WINDOW_DAYS = 90
LAG = 3

# Monitoring configuration
DRIFT_THRESHOLD_PERCENT = 10.0