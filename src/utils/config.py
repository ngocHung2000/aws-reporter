import json
from utils.logging import setup_logging

logger = setup_logging()

class Config:
    @staticmethod
    def load_config(file_path: str):
        """Load configuration from JSON file"""
        try:
            with open(file_path, "r") as config_file:
                config = json.load(config_file)
                logger.info("Configuration loaded successfully.")
                return config
        except Exception as e:
            logger.error(f"Failed to load configuration from {file_path}: {str(e)}")
            raise
