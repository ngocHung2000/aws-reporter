from utils.logging import setup_logging
from .aws_base_service import AWSBaseService

logger = setup_logging()

class AWSEC2Service(AWSBaseService):
    def __init__(self, session=None):
        super().__init__(session)

    def get_resources(self):
        """Retrieve EC2 instances based on configuration"""
        response = self.session.client("ec2").describe_instances()
        return response
    
    def start_instance(self, instance_id: str):
        """Start an EC2 instance"""
        try:
            self.session.client("ec2").start_instances(InstanceIds=[instance_id])
            logger.info(f"Started instance {instance_id} successfully.")
        except Exception as e:
            logger.error(f"Failed to start instance {instance_id}: {str(e)}")
            raise
    
    def stop_instance(self, instance_id: str):
        """Stop an EC2 instance"""
        try:
            self.session.client("ec2").stop_instances(InstanceIds=[instance_id])
            logger.info(f"Stopped instance {instance_id} successfully.")
        except Exception as e:
            logger.error(f"Failed to stop instance {instance_id}: {str(e)}")
            raise