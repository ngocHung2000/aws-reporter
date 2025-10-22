from utils.logging import setup_logging
from models.Config import Config

logger = setup_logging()

account_config = Config.load_config("config/accounts.json")
logger.info(f"Loaded account configuration: {account_config}")