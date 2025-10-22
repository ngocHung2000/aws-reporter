import logging
import os
from datetime import datetime

def setup_logging():
    # Configure logging format
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        level=logging.INFO, 
        format=log_format,
        handlers=[logging.StreamHandler()]
    )