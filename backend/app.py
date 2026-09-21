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
from http.server import HTTPServer, BaseHTTPRequestHandler

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


class RequestHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        engine = RailBlockDualEngine(DEMO_MAINTENANCE_REQUESTS, DEMO_LIVE_TRAINS)

        if self.path == '/' or self.path == '/index.html' or self.path.startswith('/?'):
            if os.path.exists(FRONTEND_INDEX):
                self.send_response(200)
                self._send_cors_headers()
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(FRONTEND_INDEX, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Frontend index.html not found.")

        elif self.path.startswith('/assets/'):
            asset_path = os.path.join(FRONTEND_DIR, self.path.lstrip('/'))
            if os.path.exists(asset_path) and os.path.isfile(asset_path):
                self.send_response(200)
                self._send_cors_headers()
                self.send_header('Content-Type', _get_mime_type(asset_path))
                self.end_headers()
                with open(asset_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()

        elif self.path == '/api/optimize':
            self._respond_json(engine.optimize_maintenance())

        elif self.path == '/api/dispatch':
            self._respond_json(engine.optimize_dispatching())

        elif self.path.startswith('/api/full-pipeline'):
            self._respond_json(engine.run_full_pipeline())

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

            new_req = MaintenanceRequest(
                id=f"REQ-{len(DEMO_MAINTENANCE_REQUESTS)+1:02d}",
                department=str(data.get("department", "P-Way (Engineering)")),
                section=str(data.get("section", "Delhi-Mathura Section")),
                preferred_start_hour=preferred_start,
                duration_hours=duration,
                priority=priority
            )
            DEMO_MAINTENANCE_REQUESTS.append(new_req)
            
            engine = RailBlockDualEngine(DEMO_MAINTENANCE_REQUESTS, DEMO_LIVE_TRAINS)
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

            engine = RailBlockDualEngine(DEMO_MAINTENANCE_REQUESTS, DEMO_LIVE_TRAINS)
            result = engine.run_full_pipeline()
            self._respond_json(result, status_code=200)

        else:
            self.send_response(404)
            self.end_headers()

    def _respond_json(self, data: dict, status_code: int = 200):
        self.send_response(status_code)
        self._send_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run_server(start_port=8080):
    for port in range(start_port, start_port + 20):
        try:
            server_address = ('', port)
            HTTPServer.allow_reuse_address = True
            httpd = HTTPServer(server_address, RequestHandler)
            print(f"🚆 RailBlock-AI Server running at http://localhost:{port}")
            httpd.serve_forever()
            break
        except OSError as e:
            if e.errno == 48:
                continue
            else:
                raise e

if __name__ == '__main__':
    run_server()
