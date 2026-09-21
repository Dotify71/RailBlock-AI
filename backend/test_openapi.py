import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import OPENAPI_SPEC, SWAGGER_UI_HTML

class TestOpenAPISpec(unittest.TestCase):
    def test_openapi_spec_structure(self):
        self.assertEqual(OPENAPI_SPEC["openapi"], "3.0.3")
        self.assertIn("info", OPENAPI_SPEC)
        self.assertIn("paths", OPENAPI_SPEC)
        self.assertIn("/api/optimize", OPENAPI_SPEC["paths"])
        self.assertIn("/api/dispatch", OPENAPI_SPEC["paths"])
        self.assertIn("/api/full-pipeline", OPENAPI_SPEC["paths"])
        self.assertIn("/api/requests", OPENAPI_SPEC["paths"])
        self.assertIn("/api/trains", OPENAPI_SPEC["paths"])

    def test_swagger_ui_html_content(self):
        self.assertIn("swagger-ui", SWAGGER_UI_HTML)
        self.assertIn("/api/openapi.json", SWAGGER_UI_HTML)

if __name__ == '__main__':
    unittest.main()
