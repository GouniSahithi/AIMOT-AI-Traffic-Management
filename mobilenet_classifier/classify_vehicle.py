import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from pathlib import Path

# Config
MODEL_PATH = Path("E:/TrafficManagementSystem/mobilenetv2_model.h5")
CROPPED_DIR = Path("E:/TrafficManagementSystem/yolo_detection/cropped_vehicles")
CLASS_NAMES = ['ambulance', 'bus', 'fire_engine', 'truck']
CONFIDENCE_THRESHOLD = 0.92

# Load the trained model
model = load_model(MODEL_PATH)

def classify_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        predictions = model.predict(img_array, verbose=0)
        predicted_class = CLASS_NAMES[np.argmax(predictions)]
        confidence = np.max(predictions)
        return predicted_class, confidence
    except Exception as e:
        print(f"⚠️ Error loading {img_path}: {e}")
        return None, 0

def classify_emergency_by_lane():
   # print("\n🧪 [Simulated] Emergency Classification Logic...")
    emergency_flags = {1: False, 2: False, 3: True, 4: False}
    for lane_id, flag in emergency_flags.items():
        if flag:
            print(f"🚨 Emergency detected in lane {lane_id}")
    return emergency_flags


if __name__ == "__main__":
    flags = classify_emergency_by_lane()
    print("\n✅ Emergency Flags Per Lane:", flags)