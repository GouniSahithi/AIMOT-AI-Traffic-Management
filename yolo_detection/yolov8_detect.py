import cv2
import os
from ultralytics import YOLO
from pathlib import Path

# Path config
VIDEO_DIR = Path("E:/TrafficManagementSystem/input_videos")
CROPPED_DIR = Path("cropped_vehicles")
CROPPED_DIR.mkdir(exist_ok=True)
LANE_DENSITY = {}  # {lane_id: [density values]}
EMERGENCY_CROPS = {}  # {lane_id: [cropped image paths]}

# Load YOLOv8 (Nano version for speed, or use yolov8s/m/l)
model = YOLO('yolov8n.pt')
EMERGENCY_CLASSES = ['bus', 'truck']
COCO_CLASS_MAP = model.names  # COCO index-to-class map

def process_lane_video(lane_id, video_path):
    print(f"➡️ [Lane {lane_id}] Opening video: {video_path}")
    cap = cv2.VideoCapture(str(video_path))
    frame_count = 0
    lane_density = []
    emergency_crop_paths = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        results = model.predict(frame, conf=0.4, verbose=False)
        detections = results[0].boxes.data

        total_area = 0
        for i, det in enumerate(detections):
            x1, y1, x2, y2, conf, cls = det
            cls = int(cls.item())
            class_name = COCO_CLASS_MAP[cls]
            box_area = (x2 - x1) * (y2 - y1)
            total_area += box_area

            if class_name in EMERGENCY_CLASSES and box_area > 50000:
                # Crop and save vehicle image for MobileNetV2
                crop = frame[int(y1):int(y2), int(x1):int(x2)]
                crop_filename = f"{CROPPED_DIR}/lane{lane_id}_frame{frame_count}_{i}.jpg"
                cv2.imwrite(crop_filename, crop)
                emergency_crop_paths.append(str(crop_filename))

        lane_density.append(total_area)

    cap.release()
    LANE_DENSITY[lane_id] = lane_density
    EMERGENCY_CROPS[lane_id] = emergency_crop_paths
    print(f"✅ Finished processing Lane {lane_id}: {len(lane_density)} frames")

def main():
    print("🚀 Starting lane processing...")  
    for lane_id in range(1, 5):
        video_path = VIDEO_DIR / f"lane{lane_id}.mp4"
        print(f"🔍 Checking for: {video_path}")
        if not video_path.exists():
            print(f"⚠️ Lane {lane_id} video not found!")
            continue
        print(f"📹 Processing Lane {lane_id}...") 
        process_lane_video(lane_id, video_path)

    # After all lanes processed
    print("✅ All lanes processed.")
    print("🔢 LANE_DENSITY Summary:", {k: len(v) for k, v in LANE_DENSITY.items()})
    print("🛑 EMERGENCY_CROPS Summary:", {k: len(v) for k, v in EMERGENCY_CROPS.items()})

    import json

    # Print full raw LANE_DENSITY values for copy-paste
    print("\n📊 Raw LANE_DENSITY Values:")
    # Convert tensors inside LANE_DENSITY to floats for JSON serialization
    lane_density_serializable = {
        k: [float(v) for v in values] for k, values in LANE_DENSITY.items()
    }

    print(json.dumps(lane_density_serializable, indent=4))



if __name__ == "__main__":
    main()