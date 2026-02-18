import os
import shutil
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from pathlib import Path
import cv2

# Config
MODEL_PATH = Path("E:/TrafficManagementSystem/mobilenetv2_model.h5")
CROPPED_DIR = Path("E:/TrafficManagementSystem/yolo_detection/cropped_vehicles")
DATASET_DIR = Path("E:/TrafficManagementSystem/classification_dataset")
CLASS_NAMES = ['ambulance', 'bus', 'fire_engine', 'truck']
CONFIDENCE_THRESHOLD = 0.9
LANES_TO_REVIEW = [1, 2]  # Misclassified lanes

# Load model
model = load_model(MODEL_PATH)

def classify_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array, verbose=0)
    predicted_class = CLASS_NAMES[np.argmax(predictions)]
    confidence = np.max(predictions)
    return predicted_class, confidence

def review_lane(lane_id):
    print(f"\n🔍 Reviewing Lane {lane_id}")
    for file in CROPPED_DIR.glob(f"lane{lane_id}_*.jpg"):
        label, conf = classify_image(file)
        if label == "ambulance" and conf >= CONFIDENCE_THRESHOLD:
            print(f"🚨 Detected: {file.name} → {label} ({conf:.2f})")

            # Show image
            img = cv2.imread(str(file))
            cv2.imshow(f"Is this actually an ambulance? [y = yes, n = no, q = quit]", img)
            key = cv2.waitKey(0)

            if key == ord('y'):
                print("✅ Confirmed as ambulance.")
            elif key == ord('n'):
                # Ask: truck or bus?
                print("❌ Misclassified! Press 't' for truck or 'b' for bus.")
                key2 = cv2.waitKey(0)
                if key2 == ord('t'):
                    dest = DATASET_DIR / "truck" / file.name
                elif key2 == ord('b'):
                    dest = DATASET_DIR / "bus" / file.name
                else:
                    print("⚠️ Invalid class, skipping...")
                    continue

                shutil.copy(str(file), str(dest))
                print(f"➡️ Moved to: {dest}")
            elif key == ord('q'):
                print("❌ Quit review.")
                break

            cv2.destroyAllWindows()

if __name__ == "__main__":
    for lane in LANES_TO_REVIEW:
        review_lane(lane)
    print("✅ Review complete. You can now retrain your model.")
