import os
import sys
import unittest
import logging

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import logger

class TestStructuredLogging(unittest.TestCase):
    def test_logger_configuration(self):
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "RailBlock-AI")

if __name__ == '__main__':
    unittest.main()
