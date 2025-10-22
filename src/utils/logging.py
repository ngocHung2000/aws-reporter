import logging
import os
from datetime import datetime

def setup_logging():
    # Configure logging format
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    if os.getenv("AWS_LAMBDA_LOG_GROUP_NAME") or os.getenv("AWS_LAMBDA_LOG_STREAM_NAME"):
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[logging.StreamHandler()]
        )
    else:
        try:
            os.makedirs("logs", exist_ok=True)
            logging.basicConfig(
                level=log_level,
                format=log_format,
                handlers=[
                    logging.FileHandler(f"logs/app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                    logging.StreamHandler()
                ]
            )
        except PermissionError:
            logging.basicConfig(
                level=log_level,
                format=log_format,
                handlers=[logging.StreamHandler()]
            )
    return logging.getLogger(__name__)