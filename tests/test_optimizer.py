"""
Unit tests for RailBlock-AI Dual-Engine Optimizer Core (backend/optimizer.py).
"""

import unittest
from backend.optimizer import (
    RailBlockDualEngine,
    MaintenanceRequest,
    TrainStatus,
    ConsolidatedBlock,
    DispatcherRecommendation
)


class TestRailBlockOptimizer(unittest.TestCase):

    def test_optimize_maintenance_empty(self):
        """Test optimize_maintenance with zero requests."""
        engine = RailBlockDualEngine([], [])
        result = engine.optimize_maintenance()
        
        self.assertIn("summary", result)
        self.assertIn("optimized_blocks", result)
        self.assertEqual(result["summary"]["total_requests"], 0)
        self.assertEqual(result["summary"]["total_consolidated_blocks"], 0)
        self.assertEqual(result["summary"]["original_total_shutdown_hours"], 0)
        self.assertEqual(len(result["optimized_blocks"]), 0)

    def test_optimize_maintenance_single_request(self):
        """Test optimize_maintenance with a single maintenance request."""
        reqs = [
            MaintenanceRequest("REQ-01", "P-Way", "Delhi-Mathura Section", 10, 3, 1)
        ]
        engine = RailBlockDualEngine(reqs, [])
        result = engine.optimize_maintenance()

        self.assertEqual(result["summary"]["total_requests"], 1)
        self.assertEqual(result["summary"]["total_consolidated_blocks"], 1)
        self.assertEqual(result["summary"]["original_total_shutdown_hours"], 3)
        self.assertEqual(len(result["optimized_blocks"]), 1)
        
        block = result["optimized_blocks"][0]
        self.assertEqual(block["section"], "Delhi-Mathura Section")
        self.assertEqual(block["start_hour"], 10)
        self.assertEqual(block["duration_hours"], 3)
        self.assertIn("REQ-01", block["original_requests"])

    def test_optimize_maintenance_overlapping_requests(self):
        """Test optimize_maintenance with overlapping multi-department requests."""
        reqs = [
            MaintenanceRequest("REQ-01", "P-Way", "Delhi-Mathura Section", 10, 3, 1),
            MaintenanceRequest("REQ-02", "TRD", "Delhi-Mathura Section", 11, 2, 2),
            MaintenanceRequest("REQ-03", "S&T", "Delhi-Mathura Section", 12, 2, 1)
        ]
        engine = RailBlockDualEngine(reqs, [])
        result = engine.optimize_maintenance()

        # Should consolidate overlapping requests into 1 joint window (hours 10 to 14 = 4 hours duration)
        self.assertEqual(result["summary"]["total_requests"], 3)
        self.assertEqual(result["summary"]["total_consolidated_blocks"], 1)
        self.assertEqual(result["summary"]["original_total_shutdown_hours"], 7)
        self.assertEqual(result["summary"]["optimized_total_shutdown_hours"], 4)

        block = result["optimized_blocks"][0]
        self.assertEqual(block["start_hour"], 10)
        self.assertEqual(block["end_hour"], 14)
        self.assertEqual(block["duration_hours"], 4)
        self.assertEqual(sorted(block["departments_covered"]), ["P-Way", "S&T", "TRD"])

    def test_optimize_maintenance_non_overlapping_requests(self):
        """Test optimize_maintenance with non-overlapping requests on same section."""
        reqs = [
            MaintenanceRequest("REQ-01", "P-Way", "Delhi-Mathura Section", 8, 2, 1),
            MaintenanceRequest("REQ-02", "TRD", "Delhi-Mathura Section", 16, 3, 2)
        ]
        engine = RailBlockDualEngine(reqs, [])
        result = engine.optimize_maintenance()

        self.assertEqual(result["summary"]["total_requests"], 2)
        self.assertEqual(result["summary"]["total_consolidated_blocks"], 2)
        self.assertEqual(len(result["optimized_blocks"]), 2)

    def test_optimize_dispatching_no_delays(self):
        """Test optimize_dispatching when all trains are on time."""
        trains = [
            TrainStatus("12004", "Shatabdi Exp", "Superfast Express", "NDLS", "FDB", delay_minutes=0, speed_kmh=110, priority=1),
            TrainStatus("12952", "Rajdhani Exp", "Rajdhani/Vande Bharat", "NDLS", "FDB", delay_minutes=0, speed_kmh=120, priority=1)
        ]
        engine = RailBlockDualEngine([], trains)
        result = engine.optimize_dispatching()

        self.assertEqual(result["summary"]["delayed_trains_detected"], 0)
        self.assertEqual(result["summary"]["overtake_actions_generated"], 0)
        self.assertEqual(len(result["dispatch_recommendations"]), 0)

    def test_optimize_dispatching_with_overtake_recommendation(self):
        """Test optimize_dispatching when a delayed freight train impedes an express train."""
        trains = [
            TrainStatus("G-501", "Freight Goods", "Goods Freight", "FDB", "PWL", delay_minutes=25, speed_kmh=45, priority=3),
            TrainStatus("12952", "Rajdhani Exp", "Rajdhani/Vande Bharat", "NDLS", "FDB", delay_minutes=2, speed_kmh=120, priority=1)
        ]
        engine = RailBlockDualEngine([], trains)
        result = engine.optimize_dispatching()

        self.assertEqual(result["summary"]["delayed_trains_detected"], 1)
        self.assertEqual(result["summary"]["overtake_actions_generated"], 1)
        self.assertEqual(len(result["dispatch_recommendations"]), 1)

        rec = result["dispatch_recommendations"][0]
        self.assertEqual(rec["action_station"], "Palwal (PWL)")
        self.assertEqual(rec["siding_track"], "Loop Line 2")
        self.assertIn("12952 (Rajdhani Exp)", rec["overtaking_trains"][0])

    def test_run_full_pipeline(self):
        """Test run_full_pipeline execution."""
        engine = RailBlockDualEngine([], [])
        result = engine.run_full_pipeline()

        self.assertIn("feature1_maintenance_optimization", result)
        self.assertIn("feature2_ai_train_dispatcher", result)


if __name__ == "__main__":
    unittest.main()
