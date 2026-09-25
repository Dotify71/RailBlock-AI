"""
RailBlock-AI Dual-Feature REST Server
Provides endpoints for:
1. Joint Maintenance Window Clustering (/api/optimize)
2. AI Train Dispatcher & Overtake Engine (/api/dispatch)
3. Combined Pipeline (/api/full-pipeline)
4. Health Check (/healthz or /api/health)
5. Add/Update Maintenance Request (/api/requests)
6. Add/Update Train Status (/api/trains)
"""

import json
import os
import sys
import threading
from http.server import HTTPServer, ThreadingHTTPServer, BaseHTTPRequestHandler

# Mutex lock protecting shared in-memory state across concurrent request threads
DATA_LOCK = threading.Lock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from optimizer import (
        RailBlockDualEngine,
        DEMO_MAINTENANCE_REQUESTS,
        DEMO_LIVE_TRAINS,
        MaintenanceRequest,
        TrainStatus
    )
except ImportError:
    from .optimizer import (
        RailBlockDualEngine,
        DEMO_MAINTENANCE_REQUESTS,
        DEMO_LIVE_TRAINS,
        MaintenanceRequest,
        TrainStatus
    )

FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
FRONTEND_INDEX = os.path.join(FRONTEND_DIR, "index.html")

MIME_TYPES = {
    # Images
    ".svg":   "image/svg+xml",
    ".png":   "image/png",
    ".jpg":   "image/jpeg",
    ".jpeg":  "image/jpeg",
    ".gif":   "image/gif",
    ".webp":  "image/webp",
    ".ico":   "image/x-icon",
    # Scripts and styles
    ".js":    "application/javascript",
    ".css":   "text/css; charset=utf-8",
    # Data and markup
    ".json":  "application/json",
    ".xml":   "application/xml",
    ".html":  "text/html; charset=utf-8",
    ".txt":   "text/plain; charset=utf-8",
    # Fonts
    ".woff":  "font/woff",
    ".woff2": "font/woff2",
    ".ttf":   "font/ttf",
    ".otf":   "font/otf",
}

def _get_mime_type(path: str) -> str:
    _, ext = os.path.splitext(path)
    return MIME_TYPES.get(ext.lower(), "application/octet-stream")

# CORS origin policy.
# In development the wildcard default allows any browser to reach the API.
# For production, set the ALLOWED_ORIGIN environment variable to the specific
# origin of your dashboard host, e.g.:
#   export ALLOWED_ORIGIN=https://dashboard.railblock.internal
# This value is read once at startup so all requests share the same policy.
ALLOWED_ORIGIN: str = os.getenv("ALLOWED_ORIGIN", "*")

import time
from collections import defaultdict

# Rate Limiter Configuration: 60 requests per 60 seconds per IP
RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_WINDOW_SECONDS = 60

import threading

class RateLimiter:
    def __init__(self, max_requests: int = RATE_LIMIT_REQUESTS, window_seconds: int = RATE_LIMIT_WINDOW_SECONDS):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
        self._lock = threading.Lock()
        self._counter = 0

    def is_allowed(self, ip: str) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds
        
        with self._lock:
            # Periodic cleanup to prevent unbounded memory leak
            self._counter += 1
            if self._counter > 1000:
                self._counter = 0
                stale = [k for k, v in self.requests.items() if not v or v[-1] <= cutoff]
                for k in stale:
                    self.requests.pop(k, None)
                    
            valid_ts = [ts for ts in self.requests[ip] if ts > cutoff]
            if len(valid_ts) >= self.max_requests:
                self.requests[ip] = valid_ts
                return False

            valid_ts.append(now)
            self.requests[ip] = valid_ts
            return True

RATE_LIMITER = RateLimiter()


class RequestHandler(BaseHTTPRequestHandler):
    def _check_rate_limit(self) -> bool:
        client_ip = self.client_address[0] if self.client_address else "127.0.0.1"
        if not RATE_LIMITER.is_allowed(client_ip):
            self._respond_json(
                {"error": "Too Many Requests", "message": "Rate limit exceeded. Maximum 60 requests per minute allowed."},
                status_code=429
            )
            return False
        return True

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-XSS-Protection", "1; mode=block")

        # When a specific origin is configured (not the wildcard), tell caching
        # proxies that the response varies by origin.  Without this header, a
        # proxy could serve a cached response intended for one origin to a
        # completely different one, bypassing the restriction entirely.
        if ALLOWED_ORIGIN != "*":
            self.send_header("Vary", "Origin")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html' or self.path.startswith('/?'):
            if os.path.exists(FRONTEND_INDEX):
                self.send_response(200)
                self._send_cors_headers()
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                try:
                    with open(FRONTEND_INDEX, 'rb') as f:
                        self.wfile.write(f.read())
                except (BrokenPipeError, ConnectionResetError):
                    pass
            else:
                self.send_response(404)
                self.end_headers()
                try:
                    self.wfile.write(b"Frontend index.html not found.")
                except (BrokenPipeError, ConnectionResetError):
                    pass

        elif self.path.startswith('/assets/'):
            asset_path = os.path.join(FRONTEND_DIR, self.path.lstrip('/'))
            if os.path.exists(asset_path) and os.path.isfile(asset_path):
                self.send_response(200)
                self._send_cors_headers()
                self.send_header('Content-Type', _get_mime_type(asset_path))
                self.end_headers()
                try:
                    with open(asset_path, 'rb') as f:
                        self.wfile.write(f.read())
                except (BrokenPipeError, ConnectionResetError):
                    pass
            else:
                self.send_response(404)
                self.end_headers()

        elif self.path == '/api/optimize':
            with DATA_LOCK:
                engine = RailBlockDualEngine(list(DEMO_MAINTENANCE_REQUESTS), list(DEMO_LIVE_TRAINS))
                result = engine.optimize_maintenance()
            self._respond_json(result)

        elif self.path == '/api/dispatch':
            with DATA_LOCK:
                engine = RailBlockDualEngine(list(DEMO_MAINTENANCE_REQUESTS), list(DEMO_LIVE_TRAINS))
                result = engine.optimize_dispatching()
            self._respond_json(result)

        elif self.path.startswith('/api/full-pipeline'):
            with DATA_LOCK:
                engine = RailBlockDualEngine(list(DEMO_MAINTENANCE_REQUESTS), list(DEMO_LIVE_TRAINS))
                result = engine.run_full_pipeline()
            self._respond_json(result)

        elif self.path == '/healthz' or self.path == '/api/health':
            self._respond_json({"status": "healthy", "service": "RailBlock-AI Core Engine"}, status_code=200)

        else:
            self.send_response(404)
            self.end_headers()

    def _parse_json_body(self):
        """Safely read and parse incoming JSON request body."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self._respond_json({"error": "Invalid JSON payload"}, status_code=400)
                return None
            body = self.rfile.read(content_length)
            data = json.loads(body)
            if not isinstance(data, dict):
                self._respond_json({"error": "Invalid JSON payload"}, status_code=400)
                return None
            return data
        except (ValueError, json.JSONDecodeError):
            self._respond_json({"error": "Invalid JSON payload"}, status_code=400)
            return None

    def do_POST(self):
        if not self._check_rate_limit():
            return

        if self.path == '/api/requests':
            data = self._parse_json_body()
            if data is None:
                return

            try:
                preferred_start = int(data.get("preferred_start_hour", 10))
                duration = int(data.get("duration_hours", 2))
                priority = int(data.get("priority", 1))
            except (ValueError, TypeError):
                self._respond_json({"error": "Invalid numeric values in request payload"}, status_code=400)
                return

            if not (0 <= preferred_start <= 23) or duration <= 0 or not (1 <= priority <= 3):
                self._respond_json({"error": "preferred_start_hour must be 0-23, duration_hours > 0, priority 1-3"}, status_code=400)
                return

            with DATA_LOCK:
                new_req = MaintenanceRequest(
                    id=f"REQ-{len(DEMO_MAINTENANCE_REQUESTS)+1:02d}",
                    department=str(data.get("department", "P-Way (Engineering)")),
                    section=str(data.get("section", "Delhi-Mathura Section")),
                    preferred_start_hour=preferred_start,
                    duration_hours=duration,
                    priority=priority
                )
                DEMO_MAINTENANCE_REQUESTS.append(new_req)
                
                engine = RailBlockDualEngine(list(DEMO_MAINTENANCE_REQUESTS), list(DEMO_LIVE_TRAINS))
                result = engine.run_full_pipeline()
            self._respond_json(result, status_code=201)

        elif self.path == '/api/trains':
            data = self._parse_json_body()
            if data is None:
                return

            raw_train_no = data.get("train_number")
            if not raw_train_no:
                self._respond_json({"error": "train_number is required"}, status_code=400)
                return
            train_no = str(raw_train_no).strip()

            try:
                delay = int(data.get("delay_minutes", 0))
                speed = int(data.get("speed_kmh", 80))
                priority = int(data.get("priority", 2))
            except (ValueError, TypeError):
                self._respond_json({"error": "Invalid numeric values in request payload"}, status_code=400)
                return

            with DATA_LOCK:
                found = False
                for t in DEMO_LIVE_TRAINS:
                    if t.train_number == train_no:
                        t.delay_minutes = delay
                        t.speed_kmh = speed
                        t.priority = priority
                        found = True
                        break
                
                if not found:
                    DEMO_LIVE_TRAINS.append(TrainStatus(
                        train_number=train_no,
                        train_name=str(data.get("train_name", "Express Special")),
                        category=str(data.get("category", "Superfast Express")),
                        current_station=str(data.get("current_station", "Faridabad (FDB)")),
                        next_station=str(data.get("next_station", "Palwal (PWL)")),
                        delay_minutes=delay,
                        speed_kmh=speed,
                        priority=priority
                    ))

                engine = RailBlockDualEngine(list(DEMO_MAINTENANCE_REQUESTS), list(DEMO_LIVE_TRAINS))
                result = engine.run_full_pipeline()
            self._respond_json(result, status_code=200)

        else:
            self.send_response(404)
            self.end_headers()

    def _respond_json(self, data: dict, status_code: int = 200):
        try:
            self.send_response(status_code)
            self._send_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError):
            pass

def run_server(start_port=8080):
    """Start the server, trying successive ports if the preferred one is in use.

    ThreadingHTTPServer spawns a new thread for every incoming request, so
    slow optimizer calls or concurrent dashboard refreshes no longer block
    each other.
    """

    # Set allow_reuse_address on our own subclass so we do not mutate the
    # standard-library class directly.
    class _Server(ThreadingHTTPServer):
        allow_reuse_address = True

    # Port-in-use errno values differ across platforms.
    PORT_IN_USE_ERRNOS = {48, 98}  # 48 = macOS/BSD, 98 = Linux

    for port in range(start_port, start_port + 20):
        try:
            server_address = ('', port)
            httpd = _Server(server_address, RequestHandler)
            print(f"RailBlock-AI server running at http://localhost:{port}")
            httpd.serve_forever()
            break
        except OSError as e:
            if e.errno in PORT_IN_USE_ERRNOS:
                continue
            raise

if __name__ == '__main__':
    run_server()
