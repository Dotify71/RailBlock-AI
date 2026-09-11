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
                if asset_path.endswith('.svg'):
                    self.send_header('Content-Type', 'image/svg+xml')
                elif asset_path.endswith('.jpg') or asset_path.endswith('.jpeg'):
                    self.send_header('Content-Type', 'image/jpeg')
                elif asset_path.endswith('.png'):
                    self.send_header('Content-Type', 'image/png')
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
            result = engine.run_full_pipeline()
            self._respond_json(result, status_code=201)

        elif self.path == '/api/trains':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            train_no = data.get("train_number")
            delay = int(data.get("delay_minutes", 0))

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
                    speed_kmh=int(data.get("speed_kmh", 80)),
                    priority=int(data.get("priority", 2))
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
