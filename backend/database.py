"""
RailBlock-AI Database Manager
Provides SQLite database persistence for maintenance requests and train telemetry states.
"""

import os
import sqlite3
import sys
from typing import List

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from optimizer import (
        MaintenanceRequest,
        TrainStatus,
        DEMO_MAINTENANCE_REQUESTS,
        DEMO_LIVE_TRAINS
    )
except ImportError:
    from .optimizer import (
        MaintenanceRequest,
        TrainStatus,
        DEMO_MAINTENANCE_REQUESTS,
        DEMO_LIVE_TRAINS
    )

DEFAULT_DB_PATH = os.getenv(
    "RAILBLOCK_DB_PATH",
    os.path.join(BASE_DIR, "railblock.db")
)


def get_connection(db_path: str = None) -> sqlite3.Connection:
    """Establish and return a SQLite database connection with row dictionary access."""
    path = db_path or DEFAULT_DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = None):
    """Initialize database tables and seed with initial demo data if empty."""
    conn = get_connection(db_path)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS maintenance_requests (
                id TEXT PRIMARY KEY,
                department TEXT NOT NULL,
                section TEXT NOT NULL,
                preferred_start_hour INTEGER NOT NULL,
                duration_hours INTEGER NOT NULL,
                priority INTEGER NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS train_statuses (
                train_number TEXT PRIMARY KEY,
                train_name TEXT NOT NULL,
                category TEXT NOT NULL,
                current_station TEXT NOT NULL,
                next_station TEXT NOT NULL,
                delay_minutes INTEGER NOT NULL,
                speed_kmh INTEGER NOT NULL,
                priority INTEGER NOT NULL
            )
        """)

        # Seed initial maintenance requests if table is empty
        cursor = conn.execute("SELECT COUNT(*) as count FROM maintenance_requests")
        if cursor.fetchone()["count"] == 0:
            for req in DEMO_MAINTENANCE_REQUESTS:
                conn.execute(
                    """
                    INSERT INTO maintenance_requests
                    (id, department, section, preferred_start_hour, duration_hours, priority)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (req.id, req.department, req.section, req.preferred_start_hour, req.duration_hours, req.priority)
                )

        # Seed initial train statuses if table is empty
        cursor = conn.execute("SELECT COUNT(*) as count FROM train_statuses")
        if cursor.fetchone()["count"] == 0:
            for t in DEMO_LIVE_TRAINS:
                conn.execute(
                    """
                    INSERT INTO train_statuses
                    (train_number, train_name, category, current_station, next_station, delay_minutes, speed_kmh, priority)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (t.train_number, t.train_name, t.category, t.current_station, t.next_station, t.delay_minutes, t.speed_kmh, t.priority)
                )
    conn.close()


def get_maintenance_requests(db_path: str = None) -> List[MaintenanceRequest]:
    """Retrieve all maintenance requests from the database."""
    conn = get_connection(db_path)
    cursor = conn.execute("""
        SELECT id, department, section, preferred_start_hour, duration_hours, priority
        FROM maintenance_requests
        ORDER BY id
    """)
    rows = cursor.fetchall()
    conn.close()
    return [
        MaintenanceRequest(
            id=row["id"],
            department=row["department"],
            section=row["section"],
            preferred_start_hour=row["preferred_start_hour"],
            duration_hours=row["duration_hours"],
            priority=row["priority"]
        )
        for row in rows
    ]


def add_maintenance_request(request: MaintenanceRequest, db_path: str = None):
    """Insert or replace a maintenance request in the database."""
    conn = get_connection(db_path)
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO maintenance_requests
            (id, department, section, preferred_start_hour, duration_hours, priority)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (request.id, request.department, request.section, request.preferred_start_hour, request.duration_hours, request.priority)
        )
    conn.close()


def get_train_statuses(db_path: str = None) -> List[TrainStatus]:
    """Retrieve all train statuses from the database."""
    conn = get_connection(db_path)
    cursor = conn.execute("""
        SELECT train_number, train_name, category, current_station, next_station, delay_minutes, speed_kmh, priority
        FROM train_statuses
    """)
    rows = cursor.fetchall()
    conn.close()
    return [
        TrainStatus(
            train_number=row["train_number"],
            train_name=row["train_name"],
            category=row["category"],
            current_station=row["current_station"],
            next_station=row["next_station"],
            delay_minutes=row["delay_minutes"],
            speed_kmh=row["speed_kmh"],
            priority=row["priority"]
        )
        for row in rows
    ]


def upsert_train_status(train: TrainStatus, db_path: str = None):
    """Insert or update a train status in the database."""
    conn = get_connection(db_path)
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO train_statuses
            (train_number, train_name, category, current_station, next_station, delay_minutes, speed_kmh, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (train.train_number, train.train_name, train.category, train.current_station, train.next_station, train.delay_minutes, train.speed_kmh, train.priority)
        )
    conn.close()
