import os
import sys
import time
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import RateLimiter

class TestRateLimiter(unittest.TestCase):
    def test_rate_limiter_allows_under_limit(self):
        limiter = RateLimiter(max_requests=5, window_seconds=10)
        client_ip = "192.168.1.1"

        for i in range(5):
            self.assertTrue(limiter.is_allowed(client_ip))

    def test_rate_limiter_blocks_over_limit(self):
        limiter = RateLimiter(max_requests=3, window_seconds=10)
        client_ip = "192.168.1.2"

        self.assertTrue(limiter.is_allowed(client_ip))
        self.assertTrue(limiter.is_allowed(client_ip))
        self.assertTrue(limiter.is_allowed(client_ip))
        # 4th request should be blocked
        self.assertFalse(limiter.is_allowed(client_ip))

    def test_rate_limiter_resets_after_window(self):
        limiter = RateLimiter(max_requests=2, window_seconds=1)
        client_ip = "192.168.1.3"

        self.assertTrue(limiter.is_allowed(client_ip))
        self.assertTrue(limiter.is_allowed(client_ip))
        self.assertFalse(limiter.is_allowed(client_ip))

        time.sleep(1.1)
        # Should be allowed again after window expires
        self.assertTrue(limiter.is_allowed(client_ip))

if __name__ == '__main__':
    unittest.main()
