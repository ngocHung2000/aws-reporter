import boto3
from abc import ABC, abstractmethod
from utils.logging import setup_logging

logger = setup_logging()

class AWSBaseService(ABC):
    def __init__(self, session=None):
        if session is None:
            session = boto3.Session()
            logger.info(f"Initialized default session in account {session.client('sts').get_caller_identity().get('Account')} at region: {session.region_name}.")
        self.session = session
    @abstractmethod
    def get_resources(self):
        # Get all resources - placeholder method
        pass

    def tag_resource(self, resource_id: str, tags: dict):
        """Tagging resource"""
        try:
            tag_list = [{'Key': k, 'Value': v} for k, v in tags.items()]
            self.session.client("ec2").create_tags(Resources=[resource_id], Tags=tag_list)
            logger.info(f"Tagged resource {resource_id} with tags {tags} successfully.")
        except Exception as e:
            logger.error(f"Failed to tag resource {resource_id}: {str(e)}")
            raise