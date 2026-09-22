from ultralytics import YOLO

# Trained YOLO model
MODEL_PATH = "runs/detect/train-2/weights/best.pt"


def analyze_traffic(image_path):

    # Load trained model
    model = YOLO(MODEL_PATH)

    # Detect vehicles
    results = model.predict(
        source=image_path,
        imgsz=320,
        device="cpu",
        conf=0.5,
        verbose=False
    )

    # Vehicle counters
    car_count = 0
    heavy_count = 0

    # Count vehicles
    for result in results:
        for box in result.boxes:

            class_id = int(box.cls[0])

            if class_id == 0:
                car_count += 1

            elif class_id == 1:
                heavy_count += 1

    # Total vehicles
    vehicle_count = car_count + heavy_count

    # Traffic density
    if vehicle_count <= 3:
        density = "Low"
    elif vehicle_count <= 7:
        density = "Medium"
    else:
        density = "High"

    # Congestion prediction
    traffic_score = vehicle_count + (heavy_count * 2)

    if traffic_score <= 4:
        congestion = "Low"
    elif traffic_score <= 8:
        congestion = "Medium"
    else:
        congestion = "High"

    # Signal optimization
    if congestion == "Low":
        green_time = 30
        red_time = 30

    elif congestion == "Medium":
        green_time = 45
        red_time = 30

    else:
        green_time = 60
        red_time = 20

    # Return complete analysis
    return {
        "cars": car_count,
        "heavy_vehicles": heavy_count,
        "total_vehicles": vehicle_count,
        "density": density,
        "traffic_score": traffic_score,
        "congestion": congestion,
        "green_time": green_time,
        "red_time": red_time
    }


# Test the complete pipeline
if __name__ == "__main__":

    image_path = "dataset/test_images/traffic1.jpg"

    result = analyze_traffic(image_path)

    print("\n===== UrbanTwin AI Traffic Pipeline =====")
    print("Cars:", result["cars"])
    print("Heavy Vehicles:", result["heavy_vehicles"])
    print("Total Vehicles:", result["total_vehicles"])
    print("Traffic Density:", result["density"])
    print("Traffic Score:", result["traffic_score"])
    print("Congestion:", result["congestion"])
    print("Recommended Green Time:", result["green_time"], "seconds")
    print("Recommended Red Time:", result["red_time"], "seconds")
    print("==========================================")
    