"""
Unit tests for RailBlock-AI Database Persistence (Issue #36)
"""

import os
import tempfile
import unittest

from backend.database import (
    init_db,
    get_maintenance_requests,
    add_maintenance_request,
    get_train_statuses,
    upsert_train_status,
)
from backend.optimizer import MaintenanceRequest, TrainStatus


class TestDatabasePersistence(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_database_seeding(self):
        """Verify default demo data is seeded into SQLite database upon initialization."""
        requests = get_maintenance_requests(self.db_path)
        self.assertGreaterEqual(len(requests), 5)
        self.assertEqual(requests[0].id, "REQ-01")

        trains = get_train_statuses(self.db_path)
        self.assertGreaterEqual(len(trains), 4)

    def test_add_maintenance_request_persistence(self):
        """Verify adding a maintenance request persists in SQLite across calls."""
        new_req = MaintenanceRequest(
            id="REQ-TEST-99",
            department="S&T (Signals)",
            section="Delhi-Mathura Section",
            preferred_start_hour=14,
            duration_hours=2,
            priority=1
        )
        add_maintenance_request(new_req, self.db_path)

        # Retrieve and verify
        requests = get_maintenance_requests(self.db_path)
        req_ids = [r.id for r in requests]
        self.assertIn("REQ-TEST-99", req_ids)

        found = next(r for r in requests if r.id == "REQ-TEST-99")
        self.assertEqual(found.department, "S&T (Signals)")

    def test_upsert_train_status_persistence(self):
        """Verify inserting and updating train telemetry status persists in SQLite."""
        # Update existing train
        updated_train = TrainStatus(
            train_number="12004",
            train_name="New Delhi Shatabdi Exp",
            category="Superfast Express",
            current_station="New Delhi (NDLS)",
            next_station="Faridabad (FDB)",
            delay_minutes=45,
            speed_kmh=100,
            priority=1
        )
        upsert_train_status(updated_train, self.db_path)

        trains = get_train_statuses(self.db_path)
        shatabdi = next(t for t in trains if t.train_number == "12004")
        self.assertEqual(shatabdi.delay_minutes, 45)

        # Add brand new train
        new_train = TrainStatus(
            train_number="99999",
            train_name="Vande Bharat Express",
            category="Vande Bharat",
            current_station="Agra Cantt (AGC)",
            next_station="Gwalior (GWL)",
            delay_minutes=0,
            speed_kmh=130,
            priority=1
        )
        upsert_train_status(new_train, self.db_path)

        trains_after = get_train_statuses(self.db_path)
        vande = next(t for t in trains_after if t.train_number == "99999")
        self.assertEqual(vande.train_name, "Vande Bharat Express")


if __name__ == "__main__":
    unittest.main()
