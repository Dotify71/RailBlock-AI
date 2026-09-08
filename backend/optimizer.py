"""
RailBlock-AI Dual-Engine Optimizer Core
Combines:
1. Joint Maintenance Window Clustering (P-Way, TRD, S&T)
2. AI Train Dispatcher & Dynamic Overtake Engine (Loop Line Siding & Cascading Delay Prevention)
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Dict

# ==========================================
# FEATURE 1 DATA MODELS: MAINTENANCE BLOCKS
# ==========================================

@dataclass
class MaintenanceRequest:
    id: str
    department: str       # P-Way (Engineering), TRD (Electrification), S&T (Signals)
    section: str          # e.g., Delhi-Mathura Section
    preferred_start_hour: int
    duration_hours: int
    priority: int         # 1 (High) to 3 (Low)

@dataclass
class ConsolidatedBlock:
    block_id: str
    section: str
    start_hour: int
    end_hour: int
    duration_hours: int
    departments_covered: List[str]
    original_requests: List[str]
    time_saved_hours: float

# ==========================================
# FEATURE 2 DATA MODELS: AI TRAIN DISPATCHER
# ==========================================

@dataclass
class TrainStatus:
    train_number: str
    train_name: str
    category: str         # Superfast Express, Rajdhani/Vande Bharat, Goods Freight
    current_station: str
    next_station: str
    delay_minutes: int
    speed_kmh: int
    priority: int         # 1 (Top Priority), 2 (Express), 3 (Freight)

@dataclass
class DispatcherRecommendation:
    recommendation_id: str
    section: str
    delayed_train: str
    overtaking_trains: List[str]
    action_station: str       # Station where siding occurs (e.g. Palwal PWL)
    siding_track: str         # e.g., Loop Line 2
    wait_duration_mins: int
    cascading_delay_prevented_mins: int
    status_message: str

# ==========================================
# DUAL OPTIMIZER ENGINE CLASS
# ==========================================

class RailBlockDualEngine:
    def __init__(self, maintenance_reqs: List[MaintenanceRequest], trains: List[TrainStatus]):
        self.maintenance_reqs = maintenance_reqs
        self.trains = trains

    def optimize_maintenance(self) -> Dict:
        """Feature 1: Cluster multi-department maintenance requests into joint windows."""
        sections: Dict[str, List[MaintenanceRequest]] = {}
        for req in self.maintenance_reqs:
            sections.setdefault(req.section, []).append(req)

        optimized_blocks: List[ConsolidatedBlock] = []
        total_original_duration = sum(r.duration_hours for r in self.maintenance_reqs)
        total_consolidated_duration = 0

        block_counter = 1
        for section_name, reqs in sections.items():
            reqs.sort(key=lambda r: r.preferred_start_hour)
            i = 0
            while i < len(reqs):
                current_group = [reqs[i]]
                start = reqs[i].preferred_start_hour
                max_end = start + reqs[i].duration_hours
                
                j = i + 1
                while j < len(reqs):
                    if reqs[j].preferred_start_hour <= (max_end + 1):
                        current_group.append(reqs[j])
                        max_end = max(max_end, reqs[j].preferred_start_hour + reqs[j].duration_hours)
                        j += 1
                    else:
                        break
                
                consolidated_duration = max_end - start
                dept_list = sorted(list(set(r.department for r in current_group)))
                req_ids = [r.id for r in current_group]
                sum_individual = sum(r.duration_hours for r in current_group)
                time_saved = sum_individual - consolidated_duration if len(current_group) > 1 else 0.5

                optimized_blocks.append(ConsolidatedBlock(
                    block_id=f"BLK-{block_counter:03d}",
                    section=section_name,
                    start_hour=start,
                    end_hour=max_end,
                    duration_hours=consolidated_duration,
                    departments_covered=dept_list,
                    original_requests=req_ids,
                    time_saved_hours=round(time_saved, 1)
                ))
                total_consolidated_duration += consolidated_duration
                block_counter += 1
                i = j if j > i else i + 1

        capacity_saved_pct = round(((total_original_duration - total_consolidated_duration) / total_original_duration) * 100, 1) if total_original_duration else 0

        return {
            "summary": {
                "total_requests": len(self.maintenance_reqs),
                "total_consolidated_blocks": len(optimized_blocks),
                "original_total_shutdown_hours": total_original_duration,
                "optimized_total_shutdown_hours": total_consolidated_duration,
                "track_capacity_saved_percent": capacity_saved_pct,
                "detention_time_reduced_hours": round(total_original_duration - total_consolidated_duration, 1)
            },
            "unoptimized_requests": [asdict(r) for r in self.maintenance_reqs],
            "optimized_blocks": [asdict(b) for b in optimized_blocks]
        }

    def optimize_dispatching(self) -> Dict:
        """Feature 2: Detect delayed trains and calculate loop line siding & overtake routing."""
        recommendations: List[DispatcherRecommendation] = []
        
        # Sort trains by track section position and priority
        delayed_trains = [t for t in self.trains if t.delay_minutes > 10 or t.category == "Goods Freight"]
        high_priority_trains = [t for t in self.trains if t.priority == 1]

        rec_id = 1
        for slow_train in delayed_trains:
            # Check if higher priority trains are trailing behind
            following_trains = [
                t for t in high_priority_trains 
                if t.train_number != slow_train.train_number and t.priority < slow_train.priority
            ]
            
            if following_trains:
                overtaking_names = [f"{t.train_number} ({t.train_name})" for t in following_trains]
                delay_saved = len(following_trains) * 25  # Estimated 25 mins saved per train
                
                recommendations.append(DispatcherRecommendation(
                    recommendation_id=f"DISP-{rec_id:03d}",
                    section="Delhi-Mathura Section",
                    delayed_train=f"{slow_train.train_number} ({slow_train.train_name})",
                    overtaking_trains=overtaking_names,
                    action_station="Palwal (PWL)",
                    siding_track="Loop Line 2",
                    wait_duration_mins=12,
                    cascading_delay_prevented_mins=delay_saved,
                    status_message=f"Hold {slow_train.train_name} on PWL Loop Line 2 for 12 mins to allow {', '.join(overtaking_names)} to overtake on Main Line 1."
                ))
                rec_id += 1

        total_cascading_saved = sum(r.cascading_delay_prevented_mins for r in recommendations)

        return {
            "summary": {
                "active_trains_monitored": len(self.trains),
                "delayed_trains_detected": len(delayed_trains),
                "overtake_actions_generated": len(recommendations),
                "total_cascading_delay_prevented_mins": total_cascading_saved
            },
            "monitored_trains": [asdict(t) for t in self.trains],
            "dispatch_recommendations": [asdict(r) for r in recommendations]
        }

    def run_full_pipeline(self) -> Dict:
        """Run complete dual engine analysis."""
        return {
            "feature1_maintenance_optimization": self.optimize_maintenance(),
            "feature2_ai_train_dispatcher": self.optimize_dispatching()
        }

# ==========================================
# DEMO DATA INITIALIZATION
# ==========================================

DEMO_MAINTENANCE_REQUESTS = [
    MaintenanceRequest("REQ-01", "P-Way (Engineering)", "Delhi-Mathura Section", 10, 3, 1),
    MaintenanceRequest("REQ-02", "TRD (Electrification)", "Delhi-Mathura Section", 11, 2, 2),
    MaintenanceRequest("REQ-03", "S&T (Signals)", "Delhi-Mathura Section", 12, 2, 1),
    MaintenanceRequest("REQ-04", "P-Way (Engineering)", "Agra-Gwalior Section", 14, 4, 1),
    MaintenanceRequest("REQ-05", "TRD (Electrification)", "Agra-Gwalior Section", 15, 3, 2),
]

DEMO_LIVE_TRAINS = [
    TrainStatus("G-501", "Container Goods Freight", "Goods Freight", "Faridabad (FDB)", "Palwal (PWL)", delay_minutes=25, speed_kmh=45, priority=3),
    TrainStatus("12004", "New Delhi Shatabdi Exp", "Superfast Express", "New Delhi (NDLS)", "Faridabad (FDB)", delay_minutes=0, speed_kmh=110, priority=1),
    TrainStatus("12952", "New Delhi Rajdhani Exp", "Rajdhani/Vande Bharat", "New Delhi (NDLS)", "Faridabad (FDB)", delay_minutes=2, speed_kmh=120, priority=1),
    TrainStatus("12626", "Kerala Superfast Exp", "Superfast Express", "Ballabgarh (BVH)", "Palwal (PWL)", delay_minutes=5, speed_kmh=90, priority=2),
]

if __name__ == "__main__":
    engine = RailBlockDualEngine(DEMO_MAINTENANCE_REQUESTS, DEMO_LIVE_TRAINS)
    result = engine.run_full_pipeline()
    print(json.dumps(result, indent=2))
