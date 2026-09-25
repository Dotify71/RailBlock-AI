import os
import sys
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import RequestHandler

class TestSecurityHeaders(unittest.TestCase):
    def test_security_headers_present(self):
        handler = MagicMock(spec=RequestHandler)
        handler.send_header = MagicMock()

        RequestHandler._send_cors_headers(handler)

        calls = [call[0] for call in handler.send_header.call_args_list]
        header_names = [call[0] for call in calls]

        self.assertIn('X-Content-Type-Options', header_names)
        self.assertIn('X-Frame-Options', header_names)
        self.assertIn('X-XSS-Protection', header_names)

        headers_dict = dict(calls)
        self.assertEqual(headers_dict['X-Content-Type-Options'], 'nosniff')
        self.assertEqual(headers_dict['X-Frame-Options'], 'DENY')
        self.assertEqual(headers_dict['X-XSS-Protection'], '1; mode=block')

if __name__ == '__main__':
    unittest.main()
