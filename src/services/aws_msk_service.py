from utils.logging import setup_logging
from .aws_base_service import AWSBaseService

logger = setup_logging()

class AwsMsk(AWSBaseService):
    def __init__(self, session=None):
        super().__init__(session)

    def get_resources(self):
        """Retrieve MSK clusters"""
        response = self.session.client("kafka").list_clusters()
        return response
    
    