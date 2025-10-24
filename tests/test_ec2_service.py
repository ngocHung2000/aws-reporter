import unittest
from unittest.mock import Mock, patch
from base_test import BaseTest
from services.aws_ec2_service import AWSEC2Service

class TestEC2Service(BaseTest):
    
    def setUp(self):
        super().setUp()
        self.ec2_service = AWSEC2Service()
    
    @patch('boto3.Session')
    def test_get_resources(self, mock_session):
        # Mock EC2 client response
        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.describe_instances.return_value = {
            'Reservations': [
                {
                    'Instances': [
                        {
                            'InstanceId': 'i-1234567890abcdef0',
                            'State': {'Name': 'running'},
                            'InstanceType': 't3.micro'
                        }
                    ]
                }
            ]
        }
        
        # Test
        result = self.ec2_service.get_resources()
        
        # Assert
        self.assertIn('Reservations', result)
        self.assertEqual(len(result['Reservations']), 1)
    
    @patch('boto3.Session')
    def test_start_instance(self, mock_session):
        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client
        
        # Test
        self.ec2_service.start_instance('i-1234567890abcdef0')
        
        # Assert
        mock_client.start_instances.assert_called_once_with(
            InstanceIds=['i-1234567890abcdef0']
        )
    
    @patch('boto3.Session')
    def test_stop_instance(self, mock_session):
        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client
        
        # Test
        self.ec2_service.stop_instance('i-1234567890abcdef0')
        
        # Assert
        mock_client.stop_instances.assert_called_once_with(
            InstanceIds=['i-1234567890abcdef0']
        )

if __name__ == '__main__':
    unittest.main()
