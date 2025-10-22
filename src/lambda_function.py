from utils.logging import setup_logging
from models.config import Config
from models.aws_instance import AwsInstance
from models.aws_sts import AwsSts
logger = setup_logging()

def process_account(account):
    logger.info(f"Processing account {account['account_id']} in region {account['region']}")
    aws_instance = AwsInstance()
    instances = aws_instance.get_instances()
    logger.info(f"Retrieved {len(instances.get('Reservations', []))} reservations for account {account['account_id']}")

account_config = Config.load_config("config/accounts.json")
for account in account_config["accounts"]:
    logger.info(f"Account: {account['account_name']}, ID: {account['account_id']}")
    # session = AwsSts.assume_role(account['role_arn'], account['region'])
    process_account(account)

# logger.info(f"Loaded account configuration: {account_config}")
# aws_instance = AwsInstance(account_config, session)
# instances = aws_instance.get_instances(account_config)
