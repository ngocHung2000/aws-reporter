from utils.logging import setup_logging
from .aws_base_service import AWSBaseService

logger = setup_logging()

class AWSRDSService(AWSBaseService):
    def __init__(self, session=None):
        super().__init__(session)

    def get_resources(self):
        """Retrieve RDS instances"""
        response = self.session.client("rds").describe_db_instances()
        return response
    
    def start_db_instance(self, db_instance_identifier: str):
        """Start an RDS DB instance"""
        try:
            self.session.client("rds").start_db_instance(DBInstanceIdentifier=db_instance_identifier)
            logger.info(f"Started DB instance {db_instance_identifier} successfully.")
        except Exception as e:
            logger.error(f"Failed to start DB instance {db_instance_identifier}: {str(e)}")
            raise
    
    def stop_db_instance(self, db_instance_identifier: str):
        """Stop an RDS DB instance"""
        try:
            self.session.client("rds").stop_db_instance(DBInstanceIdentifier=db_instance_identifier)
            logger.info(f"Stopped DB instance {db_instance_identifier} successfully.")
        except Exception as e:
            logger.error(f"Failed to stop DB instance {db_instance_identifier}: {str(e)}")
            raise