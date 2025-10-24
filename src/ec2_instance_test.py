from utils.logging import setup_logging
from utils.config import Config
from services.aws_ec2_service import AWSEC2Service

logger = setup_logging()

load_config = Config.load_config("config/accounts.json")
logger.info(f"Loaded account configuration: {load_config}")

# aws_instance = AWSEC2Service()

# aws_instance.stop_instance("i-09f6dd4e8ded41cb2")
# aws_instance.start_instance("i-09f6dd4e8ded41cb2")

# tagging = {
#     "Name": "dinhnh1",
#     "Environment": "LAB",
# }
# aws_instance.tag_resource("i-09f6dd4e8ded41cb2", tagging)

# instances = aws_instance.get_instances()
# for reservation in instances['Reservations']:
#     for instance in reservation['Instances']:
#         print(f"ID: {instance['InstanceId']}, State: {instance['State']['Name']}, Type: {instance['InstanceType']}")

# with open("instances_output.json", "w") as outfile:
#     json.dump(instances, outfile, default=str, indent=4)