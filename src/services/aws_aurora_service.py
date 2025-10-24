from utils.logging import setup_logging
from .aws_base_service import AWSBaseService

logger = setup_logging()

class AuroraService(AWSBaseService):
    def __init__(self, session=None):
        super().__init__(session)

    def get_resources(self):
        """Retrieve Aurora DB clusters"""
        response = self.session.client("rds").describe_db_clusters()
        return response
    
    def start_db_cluster(self, db_cluster_identifier: str):
        """Start an Aurora DB cluster"""
        try:
            self.session.client("rds").start_db_cluster(DBClusterIdentifier=db_cluster_identifier)
            logger.info(f"Started DB cluster {db_cluster_identifier} successfully.")
        except Exception as e:
            logger.error(f"Failed to start DB cluster {db_cluster_identifier}: {str(e)}")
            raise
    
    def stop_db_cluster(self, db_cluster_identifier: str):
        """Stop an Aurora DB cluster"""
        try:
            self.session.client("rds").stop_db_cluster(DBClusterIdentifier=db_cluster_identifier)
            logger.info(f"Stopped DB cluster {db_cluster_identifier} successfully.")
        except Exception as e:
            logger.error(f"Failed to stop DB cluster {db_cluster_identifier}: {str(e)}")
            raise