import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app
from base_test import BaseTest

class TestAPI(BaseTest):
    
    def setUp(self):
        super().setUp()
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "AWS Reporter API")
    
    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")
    
    @patch('services.aws_ec2_service.AWSEC2Service.get_resources')
    def test_ec2_list_endpoint(self, mock_get_resources):
        mock_get_resources.return_value = {"Reservations": []}
        
        response = self.client.get("/api/v1/ec2/list")
        self.assertEqual(response.status_code, 200)
    
    @patch('services.aws_rds_service.AWSRDSService.get_resources')
    def test_rds_list_endpoint(self, mock_get_resources):
        mock_get_resources.return_value = {"DBInstances": []}
        
        response = self.client.get("/api/v1/rds")
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
