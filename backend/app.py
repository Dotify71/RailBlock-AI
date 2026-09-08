"""
RailBlock-AI Dual-Feature REST Server
Provides endpoints for:
1. Joint Maintenance Window Clustering (/api/optimize)
2. AI Train Dispatcher & Overtake Engine (/api/dispatch)
3. Combined Pipeline (/api/full-pipeline)
4. Where Is My Train Web Dashboard UI (/)
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from optimizer import (
    RailBlockDualEngine,
    DEMO_MAINTENANCE_REQUESTS,
    DEMO_LIVE_TRAINS,
    MaintenanceRequest
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_INDEX = os.path.join(BASE_DIR, "..", "frontend", "index.html")

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

        if self.path == '/' or self.path == '/index.html':
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

        elif self.path == '/api/optimize':
            result = engine.optimize_maintenance()
            self._respond_json(result)

        elif self.path == '/api/dispatch':
            result = engine.optimize_dispatching()
            self._respond_json(result)

        elif self.path == '/api/full-pipeline':
            result = engine.run_full_pipeline()
            self._respond_json(result)

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/requests':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            new_req = MaintenanceRequest(
                id=f"REQ-{len(DEMO_MAINTENANCE_REQUESTS)+1:02d}",
                department=data.get("department", "P-Way (Engineering)"),
                section=data.get("section", "Delhi-Mathura Section"),
                preferred_start_hour=int(data.get("preferred_start_hour", 10)),
                duration_hours=int(data.get("duration_hours", 2)),
                priority=int(data.get("priority", 1))
            )
            DEMO_MAINTENANCE_REQUESTS.append(new_req)
            
            engine = RailBlockDualEngine(DEMO_MAINTENANCE_REQUESTS, DEMO_LIVE_TRAINS)
            result = engine.optimize_maintenance()
            self._respond_json(result, status_code=201)
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
            print(f"🚆 RailBlock-AI Dual Engine Server running at http://localhost:{port}")
            print("Press Ctrl+C to stop.")
            httpd.serve_forever()
            break
        except OSError as e:
            if e.errno == 48:
                continue
            else:
                raise e

if __name__ == '__main__':
    run_server()
