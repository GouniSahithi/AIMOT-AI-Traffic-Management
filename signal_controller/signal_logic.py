# signal_logic.py

from typing import Dict

# Average crossing time (seconds) for each vehicle class
AVG_CROSS_TIME = {
    'car': 2,
    'bike': 1.5,
    'bus': 3.5,
    'truck': 3.5,
    'rickshaw': 2.5
}

# Configuration constants
MIN_GREEN = 10
MAX_GREEN = 60
EMERGENCY_GREEN = 25  # Optional override for emergency


def compute_green_time(vehicle_counts: Dict[str, int], num_lanes: int = 1) -> int:
    """
    Computes the green signal time based on vehicle counts and average crossing time.

    Args:
        vehicle_counts: Dictionary with vehicle class as key and count as value
        num_lanes: Number of lanes in that direction

    Returns:
        Calculated green time (in seconds), clamped between MIN_GREEN and MAX_GREEN
    """
    total_time = 0
    for vehicle_class, count in vehicle_counts.items():
        cross_time = AVG_CROSS_TIME.get(vehicle_class.lower(), 2)
        total_time += count * cross_time

    green_time = total_time / max(num_lanes, 1)
    return max(MIN_GREEN, min(int(green_time), MAX_GREEN))


def allocate_green_times(
    all_vehicle_counts: Dict[int, Dict[str, int]],
    emergency_flags: Dict[int, bool],
    num_lanes: Dict[int, int]
) -> Dict[int, int]:
    """
    Assigns green times to each lane based on vehicle density and emergency presence.

    Args:
        all_vehicle_counts: Dict mapping lane_id to vehicle_counts dict
        emergency_flags: Dict mapping lane_id to boolean emergency presence
        num_lanes: Dict mapping lane_id to number of lanes

    Returns:
        Dict mapping lane_id to green signal time in seconds
    """
    green_times = {}

    for lane_id, vehicle_counts in all_vehicle_counts.items():
        if emergency_flags.get(lane_id, False):
            green_times[lane_id] = max(EMERGENCY_GREEN, MIN_GREEN)
        else:
            green_times[lane_id] = compute_green_time(
                vehicle_counts, num_lanes=num_lanes.get(lane_id, 1)
            )

    return green_times


if __name__ == "__main__":
    # Sample test case
    vehicle_data = {
        1: {'car': 10, 'bike': 5, 'bus': 1},
        2: {'truck': 2, 'car': 6},
        3: {'bike': 8, 'car': 4, 'rickshaw': 3},
        4: {'car': 2, 'bus': 1, 'bike': 2}
    }

    emergency_data = {
        1: False,
        2: False,
        3: True,   # 🚨 Emergency in Lane 3
        4: False
    }

    lane_count_data = {
        1: 2,
        2: 2,
        3: 2,
        4: 2
    }

    green_signal_times = allocate_green_times(vehicle_data, emergency_data, lane_count_data)
    print("\n🚦 Green Signal Time Allocation:")
    for lane, time in green_signal_times.items():
        print(f"Lane {lane}: {time} seconds")
