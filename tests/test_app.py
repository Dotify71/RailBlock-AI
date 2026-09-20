"""
Integration tests for RailBlock-AI REST API Server (backend/app.py).
"""

import json
import threading
import time
import unittest
import urllib.request
import urllib.error
from backend.app import HTTPServer, RequestHandler


class TestRailBlockAppAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Spin up a test instance of HTTPServer on port 8995."""
        cls.port = 8995
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.server = HTTPServer(('127.0.0.1', cls.port), RequestHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        """Shutdown the test server."""
        cls.server.shutdown()

    def _make_request(self, path, method="GET", body=None, headers=None):
        if headers is None:
            headers = {}
        data = None
        if body is not None:
            if isinstance(body, (dict, list)):
                data = json.dumps(body).encode('utf-8')
                headers['Content-Type'] = 'application/json'
            elif isinstance(body, bytes):
                data = body
            elif isinstance(body, str):
                data = body.encode('utf-8')

        req = urllib.request.Request(f"{self.base_url}{path}", data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, resp.headers, resp.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            return e.code, e.headers, e.read().decode('utf-8')

    def test_get_root(self):
        """Test GET / returns HTML dashboard or 200 status."""
        status, headers, body = self._make_request("/")
        self.assertEqual(status, 200)

    def test_get_optimize_endpoint(self):
        """Test GET /api/optimize returns joint maintenance clustering results."""
        status, headers, body = self._make_request("/api/optimize")
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertIn("summary", data)
        self.assertIn("optimized_blocks", data)

    def test_get_dispatch_endpoint(self):
        """Test GET /api/dispatch returns AI dispatch recommendations."""
        status, headers, body = self._make_request("/api/dispatch")
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertIn("summary", data)
        self.assertIn("dispatch_recommendations", data)

    def test_get_full_pipeline_endpoint(self):
        """Test GET /api/full-pipeline returns complete analysis."""
        status, headers, body = self._make_request("/api/full-pipeline")
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertIn("feature1_maintenance_optimization", data)
        self.assertIn("feature2_ai_train_dispatcher", data)

    def test_get_not_found(self):
        """Test GET /nonexistent returns 404."""
        status, headers, body = self._make_request("/nonexistent")
        self.assertEqual(status, 404)

    def test_post_valid_maintenance_request(self):
        """Test POST /api/requests with valid JSON payload."""
        payload = {
            "department": "S&T (Signals)",
            "section": "Delhi-Mathura Section",
            "preferred_start_hour": 14,
            "duration_hours": 2,
            "priority": 1
        }
        status, headers, body = self._make_request("/api/requests", method="POST", body=payload)
        self.assertEqual(status, 201)
        data = json.loads(body)
        self.assertIn("feature1_maintenance_optimization", data)

    def test_post_malformed_json_request(self):
        """Test POST /api/requests with malformed JSON returns 400 Bad Request."""
        status, headers, body = self._make_request(
            "/api/requests",
            method="POST",
            body="{invalid_json}",
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(status, 400)
        data = json.loads(body)
        self.assertIn("error", data)

    def test_post_valid_train_status(self):
        """Test POST /api/trains with valid train update payload."""
        payload = {
            "train_number": "12952",
            "delay_minutes": 10,
            "speed_kmh": 105
        }
        status, headers, body = self._make_request("/api/trains", method="POST", body=payload)
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertIn("feature2_ai_train_dispatcher", data)

    def test_post_missing_train_number(self):
        """Test POST /api/trains without required train_number returns 400."""
        payload = {
            "delay_minutes": 10
        }
        status, headers, body = self._make_request("/api/trains", method="POST", body=payload)
        self.assertEqual(status, 400)
        data = json.loads(body)
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
