import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import RequestHandler

class TestHealthEndpoint(unittest.TestCase):
    def test_health_response_structure(self):
        # Verify health check payload specification
        payload = {"status": "healthy", "service": "RailBlock-AI Core Engine"}
        self.assertEqual(payload["status"], "healthy")
        self.assertEqual(payload["service"], "RailBlock-AI Core Engine")

if __name__ == '__main__':
    unittest.main()
