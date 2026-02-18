# main_pipeline.py (final version with real lane density-based vehicle data)

from signal_controller.signal_logic import allocate_green_times

# ✅ Vehicle data estimated from real LANE_DENSITY values
vehicle_data = {
    1: {'car': 52, 'bike': 17, 'bus': 8, 'truck': 8},
    2: {'car': 25, 'bike': 8, 'bus': 4, 'truck': 4},
    3: {'car': 131, 'bike': 43, 'bus': 21, 'truck': 21},  # 🚨 Emergency lane
    4: {'car': 63, 'bike': 21, 'bus': 10, 'truck': 10}
}

# ✅ Emergency vehicle present only in Lane 3
emergency_flags = {
    1: False,
    2: False,
    3: True,
    4: False
}

# ✅ Assuming 2 lanes per direction
lane_count_data = {lane_id: 2 for lane_id in vehicle_data}

# 🧠 Apply signal logic to compute green signal times
def main():
    print("\n🧠 Computing green signal times from real LANE_DENSITY-based data...")
    green_times = allocate_green_times(vehicle_data, emergency_flags, lane_count_data)

    print("\n✅ Final Green Signal Time Allocation:")
    for lane, seconds in green_times.items():
        print(f"Lane {lane}: {seconds} seconds")

if __name__ == "__main__":
    main()
