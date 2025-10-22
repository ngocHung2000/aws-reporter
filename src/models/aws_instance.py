import boto3
from .config import Config
from utils.logging import setup_logging

logger = setup_logging()

class AwsInstance:
    def __init__(self, session=None):
        if session is None:
            session = boto3.Session()
            logger.info(f"Initialized default session in account {session.client('sts').get_caller_identity().get('Account')} at region: {session.region_name}.")
        self.ec2_client = session.client("ec2")
        logger.info("AwsInstance initialized.")

    def get_instances(self):
        """Retrieve EC2 instances based on configuration"""
        response = self.ec2_client.describe_instances()
        return response
    
    def start_instance(self, instance_id: str):
        """Start an EC2 instance"""
        try:
            self.ec2_client.start_instances(InstanceIds=[instance_id])
            logger.info(f"Started instance {instance_id} successfully.")
        except Exception as e:
            logger.error(f"Failed to start instance {instance_id}: {str(e)}")
            raise
    
    def stop_instance(self, instance_id: str):
        """Stop an EC2 instance"""
        try:
            self.ec2_client.stop_instances(InstanceIds=[instance_id])
            logger.info(f"Stopped instance {instance_id} successfully.")
        except Exception as e:
            logger.error(f"Failed to stop instance {instance_id}: {str(e)}")
            raise
    
    def tag_instance(self, instance_id: str, tags: dict):
        """Tag an EC2 instance"""
        try:
            tag_list = [{'Key': k, 'Value': v} for k, v in tags.items()]
            self.ec2_client.create_tags(Resources=[instance_id], Tags=tag_list)
            logger.info(f"Tagged instance {instance_id} with tags {tags} successfully.")
        except Exception as e:
            logger.error(f"Failed to tag instance {instance_id}: {str(e)}")
            raise
