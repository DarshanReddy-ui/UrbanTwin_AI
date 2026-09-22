from ultralytics import YOLO

# Load trained model
model = YOLO("runs/detect/train/weights/best.pt")

# Test image
image_path = "dataset/valid/images/MVI_40213_img01315_jpg.rf.e061da25035aa7befbdeee2a5f1a62c0.jpg"

# Run detection
results = model.predict(
    source=image_path,
    imgsz=320,
    device="cpu",
    conf=0.5
)

# Count detected vehicles
vehicle_count = 0
car_count = 0
heavy_count = 0

for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        if class_id == 0:
            car_count += 1
        elif class_id == 1:
            heavy_count += 1

        vehicle_count += 1

# Calculate traffic density
if vehicle_count <= 3:
    density = "Low"
elif vehicle_count <= 7:
    density = "Medium"
else:
    density = "High"

print("\n===== UrbanTwin AI Traffic Analysis =====")
print("Cars:", car_count)
print("Heavy Vehicles:", heavy_count)
print("Total Vehicles:", vehicle_count)
print("Traffic Density:", density)
print("=========================================")