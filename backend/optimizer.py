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
    end_hour: int          # Always 0-23.  Read spans_midnight to know if this is next-day.
    duration_hours: int
    spans_midnight: bool   # True when the block crosses 00:00 into the following day.
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

# Standard Indian Railways main-line block section length used as the headway
# distance.  A following train that is one block section behind the slow train
# would be held for the duration it takes the slow train to clear that section.
# Overriding this constant lets the engine adapt to other network geometries.
BLOCK_SECTION_KM = 10.0

def _cascading_delay_prevented_mins(slow_speed_kmh: int, fast_speed_kmh: int) -> int:
    """Estimate cascading delay (in minutes) prevented for one overtaking train.

    When a high-priority train is trailing a slow train by one block section,
    it is effectively speed-restricted to the slow train's pace until it can
    overtake.  The delay it absorbs is the difference between the time needed
    to traverse one block section at the slow train's speed and the time it
    would have taken at its own speed.

    Formula:
        prevented_delay = (BLOCK_SECTION_KM / slow_speed - BLOCK_SECTION_KM / fast_speed) * 60

    Edge cases:
    - If the slow train's speed is 0 or negative the calculation falls back to
      a conservative 5-minute floor to avoid division by zero.
    - The result is clamped to a minimum of 1 minute so we never report zero
      or negative savings for a legitimate overtake action.
    """
    if slow_speed_kmh <= 0:
        return 5  # conservative floor when speed data is missing

    time_at_slow_speed  = BLOCK_SECTION_KM / slow_speed_kmh   # hours
    time_at_fast_speed  = BLOCK_SECTION_KM / max(fast_speed_kmh, 1)  # guard /0
    delay_hours = max(time_at_slow_speed - time_at_fast_speed, 0.0)
    delay_mins  = round(delay_hours * 60)

    # Return at least 1 minute so callers always see a non-zero saving.
    return max(delay_mins, 1)


class RailBlockDualEngine:
    def __init__(self, maintenance_reqs: List[MaintenanceRequest], trains: List[TrainStatus]):
        self.maintenance_reqs = maintenance_reqs
        self.trains = trains

    def optimize_maintenance(self) -> Dict:
        """Feature 1: Cluster multi-department maintenance requests into joint windows.

        Requests are sorted by priority first (1 = highest), then by preferred
        start hour.  This ensures that high-priority (emergency) requests anchor
        the consolidated window time rather than being pushed into a slot dictated
        by a lower-priority request that happens to start earlier.

        Midnight rollover handling
        --------------------------
        All arithmetic inside the merge loop uses linear hours (e.g. 25, 26)
        rather than clock hours (1, 2).  This keeps the overlap comparison
        ``preferred_start_hour <= max_end + 1`` correct across the day boundary.
        The clock-hour ``end_hour`` is derived with ``% 24`` only when writing
        the final ConsolidatedBlock.  ``spans_midnight`` is set to True whenever
        the raw end exceeds 24 so consumers can display the block correctly.
        """
        sections: Dict[str, List[MaintenanceRequest]] = {}
        for req in self.maintenance_reqs:
            sections.setdefault(req.section, []).append(req)

        optimized_blocks: List[ConsolidatedBlock] = []
        total_original_duration = sum(r.duration_hours for r in self.maintenance_reqs)
        total_consolidated_duration = 0

        block_counter = 1
        for section_name, reqs in sections.items():
            # Sort by priority first so Priority 1 (emergency) requests lead each
            # cluster and set the window anchor. Within the same priority level,
            # order by preferred start hour to keep the window as tight as possible.
            reqs.sort(key=lambda r: (r.priority, r.preferred_start_hour))
            i = 0
            while i < len(reqs):
                current_group = [reqs[i]]
                start = reqs[i].preferred_start_hour

                # Keep max_end in linear hours throughout the merge loop.
                # Wrapping it here would corrupt the overlap comparison below.
                max_end = start + reqs[i].duration_hours

                j = i + 1
                while j < len(reqs):
                    candidate_start = reqs[j].preferred_start_hour

                    # Normalise the candidate to linear space relative to the
                    # cluster anchor.  A request that starts earlier in clock
                    # time than the anchor (e.g. hour 10 when anchor is 23)
                    # actually belongs to the *next* calendar day from the
                    # anchor's perspective, so add 24 to keep it in the correct
                    # linear position for the overlap test.
                    if candidate_start < start:
                        candidate_start_linear = candidate_start + 24
                    else:
                        candidate_start_linear = candidate_start

                    if candidate_start_linear <= (max_end + 1):
                        current_group.append(reqs[j])
                        max_end = max(
                            max_end,
                            candidate_start_linear + reqs[j].duration_hours
                        )
                        j += 1
                    else:
                        break

                consolidated_duration = max_end - start
                dept_list = sorted({r.department for r in current_group})
                req_ids = [r.id for r in current_group]
                sum_individual = sum(r.duration_hours for r in current_group)
                time_saved = sum_individual - consolidated_duration if len(current_group) > 1 else 0.5

                # Apply midnight rollover only at the point of writing the block.
                # spans_midnight tells the caller that end_hour is a next-day time.
                crosses_midnight = max_end >= 24
                end_hour_clock = max_end % 24

                optimized_blocks.append(ConsolidatedBlock(
                    block_id=f"BLK-{block_counter:03d}",
                    section=section_name,
                    start_hour=start % 24,
                    end_hour=end_hour_clock,
                    duration_hours=consolidated_duration,
                    spans_midnight=crosses_midnight,
                    departments_covered=dept_list,
                    original_requests=req_ids,
                    time_saved_hours=round(time_saved, 1)
                ))
                total_consolidated_duration += consolidated_duration
                block_counter += 1
                i = j if j > i else i + 1

        capacity_saved_pct = round(((total_original_duration - total_consolidated_duration) / total_original_duration) * 100, 1) if total_original_duration else 0.0

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
        
        delayed_trains = [t for t in self.trains if t.delay_minutes > 10 or t.category == "Goods Freight"]
        high_priority_trains = [t for t in self.trains if t.priority == 1]

        rec_id = 1
        for slow_train in delayed_trains:
            following_trains = [
                t for t in high_priority_trains 
                if t.train_number != slow_train.train_number and t.priority < slow_train.priority
            ]
            
            if following_trains:
                overtaking_names = [f"{t.train_number} ({t.train_name})" for t in following_trains]

                # Compute delay savings individually per overtaking train based on
                # the speed differential over one block section.  This replaces the
                # previous flat 25-minute estimate with a value grounded in each
                # train's reported speed.
                per_train_savings = [
                    _cascading_delay_prevented_mins(slow_train.speed_kmh, t.speed_kmh)
                    for t in following_trains
                ]
                total_delay_saved = sum(per_train_savings)

                # The siding hold duration is the time the slow train needs to clear
                # one block section at its current speed, rounded to the nearest
                # minute.  This is the minimum time the overtaking trains must wait
                # before the main line is free.  Clamped at 1 minute.
                if slow_train.speed_kmh > 0:
                    wait_mins = max(round((BLOCK_SECTION_KM / slow_train.speed_kmh) * 60), 1)
                else:
                    wait_mins = 15  # conservative default when speed is unknown

                recommendations.append(DispatcherRecommendation(
                    recommendation_id=f"DISP-{rec_id:03d}",
                    section="Delhi-Mathura Section",
                    delayed_train=f"{slow_train.train_number} ({slow_train.train_name})",
                    overtaking_trains=overtaking_names,
                    action_station="Palwal (PWL)",
                    siding_track="Loop Line 2",
                    wait_duration_mins=wait_mins,
                    cascading_delay_prevented_mins=total_delay_saved,
                    status_message=(
                        f"Hold {slow_train.train_name} on PWL Loop Line 2 for "
                        f"{wait_mins} min(s) to allow "
                        f"{', '.join(overtaking_names)} to overtake on Main Line 1."
                    )
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
