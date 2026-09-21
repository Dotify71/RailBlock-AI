import json
import os
import sys
from http.server import BaseHTTPRequestHandler

# Ensure backend directory is in python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(BASE_DIR, "..", "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

try:
    from optimizer import (
        RailBlockDualEngine,
        DEMO_MAINTENANCE_REQUESTS,
        DEMO_LIVE_TRAINS,
        MaintenanceRequest,
        TrainStatus
    )
except ImportError:
    from backend.optimizer import (
        RailBlockDualEngine,
        DEMO_MAINTENANCE_REQUESTS,
        DEMO_LIVE_TRAINS,
        MaintenanceRequest,
        TrainStatus
    )

class handler(BaseHTTPRequestHandler):
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

        if self.path == '/api/optimize':
            result = engine.optimize_maintenance()
            self._respond_json(result)

        elif self.path == '/api/dispatch':
            result = engine.optimize_dispatching()
            self._respond_json(result)

        elif self.path.startswith('/api/full-pipeline') or self.path.startswith('/api/'):
            result = engine.run_full_pipeline()
            self._respond_json(result)

        else:
            self._respond_json({"status": "healthy", "service": "RailBlock-AI Core Engine"}, 200)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        if self.path == '/api/requests':
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
            self._respond_json(engine.run_full_pipeline(), status_code=201)

        elif self.path == '/api/trains':
            train_no = str(data.get("train_number", "G-501"))
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
            self._respond_json(engine.run_full_pipeline(), status_code=200)
        else:
            self._respond_json({"error": "Endpoint not found"}, 404)

    def _respond_json(self, data: dict, status_code: int = 200):
        self.send_response(status_code)
        self._send_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
