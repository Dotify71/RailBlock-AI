"""
RailBlock-AI Dual-Feature REST Server
Provides endpoints for:
1. Joint Maintenance Window Clustering (/api/optimize)
2. AI Train Dispatcher & Overtake Engine (/api/dispatch)
3. Combined Pipeline (/api/full-pipeline)
4. Where Is My Train Web Dashboard UI (/)
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

# Maps file extensions to their correct Content-Type values.
# Keeping this as a plain dictionary makes it easy to extend
# without touching any conditional logic elsewhere.
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
    """Return the Content-Type for a given file path.

    Falls back to application/octet-stream so the browser always receives
    a valid Content-Type header, even for unrecognised file types.
    """
    _, ext = os.path.splitext(path)
    return MIME_TYPES.get(ext.lower(), "application/octet-stream")


OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "RailBlock-AI API Specification",
        "description": "REST API for Joint Maintenance Window Clustering & AI Train Dispatcher Engine (SIH26027).",
        "version": "1.0.0"
    },
    "paths": {
        "/api/optimize": {
            "get": {
                "summary": "Run Joint Maintenance Window Clustering",
                "responses": {"200": {"description": "Optimized maintenance blocks"}}
            }
        },
        "/api/dispatch": {
            "get": {
                "summary": "Run AI Train Dispatcher & Overtake Engine",
                "responses": {"200": {"description": "Dispatch recommendations"}}
            }
        },
        "/api/full-pipeline": {
            "get": {
                "summary": "Run Joint Maintenance & Dispatching Pipeline",
                "responses": {"200": {"description": "Integrated optimization results"}}
            }
        },
        "/api/requests": {
            "post": {
                "summary": "Add or Update Maintenance Block Request",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "department": {"type": "string"},
                                    "section": {"type": "string"},
                                    "preferred_start_hour": {"type": "integer"},
                                    "duration_hours": {"type": "integer"},
                                    "priority": {"type": "integer"}
                                }
                            }
                        }
                    }
                },
                "responses": {"201": {"description": "Request created"}}
            }
        },
        "/api/trains": {
            "post": {
                "summary": "Add or Update Live Train Telemetry",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "train_number": {"type": "string"},
                                    "train_name": {"type": "string"},
                                    "delay_minutes": {"type": "integer"},
                                    "speed_kmh": {"type": "integer"},
                                    "priority": {"type": "integer"}
                                },
                                "required": ["train_number"]
                            }
                        }
                    }
                },
                "responses": {"200": {"description": "Train updated"}}
            }
        }
    }
}

SWAGGER_UI_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>RailBlock-AI API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body style="margin: 0; padding: 0;">
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        SwaggerUIBundle({
            url: '/api/openapi.json',
            dom_id: '#swagger-ui'
        });
    </script>
</body>
</html>"""


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
            result = engine.optimize_maintenance()
            self._respond_json(result)

        elif self.path == '/api/dispatch':
            result = engine.optimize_dispatching()
            self._respond_json(result)

        elif self.path.startswith('/api/full-pipeline'):
            result = engine.run_full_pipeline()
            self._respond_json(result)

        elif self.path == '/api/openapi.json':
            self._respond_json(OPENAPI_SPEC)

        elif self.path == '/api/docs' or self.path == '/api/docs/':
            self.send_response(200)
            self._send_cors_headers()
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(SWAGGER_UI_HTML.encode('utf-8'))

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

            new_req = MaintenanceRequest(
                id=f"REQ-{len(DEMO_MAINTENANCE_REQUESTS)+1:02d}",
                department=data.get("department", "P-Way (Engineering)"),
                section=data.get("section", "Delhi-Mathura Section"),
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

            train_no = data.get("train_number")
            if not train_no:
                self._respond_json({"error": "train_number is required"}, status_code=400)
                return

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
                    found = True
                    break
            
            if not found:
                DEMO_LIVE_TRAINS.append(TrainStatus(
                    train_number=train_no,
                    train_name=data.get("train_name", "Express Special"),
                    category=data.get("category", "Superfast Express"),
                    current_station=data.get("current_station", "Faridabad (FDB)"),
                    next_station=data.get("next_station", "Palwal (PWL)"),
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
