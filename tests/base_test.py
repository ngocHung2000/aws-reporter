import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.logging import setup_logging

class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.logger = setup_logging()
        cls.logger.info(f"Starting {cls.__name__} test suite")
    
    def setUp(self):
        self.logger.info(f"Running test: {self._testMethodName}")
    
    def tearDown(self):
        self.logger.info(f"Completed test: {self._testMethodName}")
