import unittest
from unittest.mock import Mock, patch
from base_test import BaseTest
from services.aws_rds_service import AWSRDSService

class TestRDSService(BaseTest):
    
    def setUp(self):
        super().setUp()
        self.rds_service = AWSRDSService()
    
    @patch('boto3.Session')
    def test_get_resources(self, mock_session):
        # Mock RDS client response
        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.describe_db_instances.return_value = {
            'DBInstances': [
                {
                    'DBInstanceIdentifier': 'test-db',
                    'DBInstanceStatus': 'available',
                    'Engine': 'mysql',
                    'DBInstanceClass': 'db.t3.micro'
                }
            ]
        }
        
        # Test
        result = self.rds_service.get_resources()
        
        # Assert
        self.assertIn('DBInstances', result)
        self.assertEqual(len(result['DBInstances']), 1)
    
    # @patch('boto3.Session')
    # def test_start_db_instance(self, mock_session):
    #     mock_client = Mock()
    #     mock_session.return_value.client.return_value = mock_client
        
    #     # Test
    #     self.rds_service.start_db_instance('test-db')
        
    #     # Assert
    #     mock_client.start_db_instance.assert_called_once_with(
    #         DBInstanceIdentifier='test-db'
    #     )
    
    # @patch('boto3.Session')
    # def test_stop_db_instance(self, mock_session):
    #     mock_client = Mock()
    #     mock_session.return_value.client.return_value = mock_client
        
    #     # Test
    #     self.rds_service.stop_db_instance('test-db')
        
    #     # Assert
    #     mock_client.stop_db_instance.assert_called_once_with(
    #         DBInstanceIdentifier='test-db'
    #     )

if __name__ == '__main__':
    unittest.main()
