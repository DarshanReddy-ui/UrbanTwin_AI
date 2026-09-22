from ultralytics import YOLO
import torch

from models.gat_model import GATModel
from models.traffic_graph import build_traffic_graph


# =====================================================
# MODEL PATHS
# =====================================================

YOLO_MODEL_PATH = "models/yolo_best.pt"
GAT_MODEL_PATH = "models/gat_traffic_model.pt"


# =====================================================
# LOAD YOLO MODEL
# =====================================================

yolo_model = YOLO(YOLO_MODEL_PATH)


# =====================================================
# LOAD GAT MODEL
# =====================================================

gat_model = GATModel(
    input_features=2,
    hidden_features=8,
    output_features=3
)

gat_model.load_state_dict(
    torch.load(
        GAT_MODEL_PATH,
        map_location="cpu"
    )
)

gat_model.eval()


# =====================================================
# TRAFFIC ANALYSIS FUNCTION
# =====================================================

def analyze_traffic(image_path):

    # -------------------------------------------------
    # YOLO VEHICLE DETECTION
    # -------------------------------------------------

    results = yolo_model.predict(
        source=image_path,
        imgsz=320,
        device="cpu",
        conf=0.5,
        verbose=False
    )


    # -------------------------------------------------
    # COUNT VEHICLES
    # -------------------------------------------------

    cars = 0
    heavy = 0

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            class_id = int(
                box.cls[0].item()
            )

            if class_id == 0:

                cars += 1

            elif class_id == 1:

                heavy += 1


    # -------------------------------------------------
    # TOTAL VEHICLES
    # -------------------------------------------------

    total_vehicles = cars + heavy


    # -------------------------------------------------
    # TRAFFIC DENSITY
    # -------------------------------------------------

    if total_vehicles <= 3:

        density = "Low"

    elif total_vehicles <= 7:

        density = "Medium"

    else:

        density = "High"


    # =================================================
    # BUILD TRAFFIC GRAPH
    # =================================================

    features, adjacency = build_traffic_graph(

        junction_402_cars=cars,
        junction_402_heavy=heavy,

        junction_405_cars=cars,
        junction_405_heavy=heavy,

        junction_219_cars=cars,
        junction_219_heavy=heavy
    )


    # =================================================
    # GAT PREDICTION
    # =================================================

    with torch.no_grad():

        gat_output = gat_model(
            features,
            adjacency
        )

        probabilities = torch.softmax(
            gat_output,
            dim=1
        )

        predictions = torch.argmax(
            gat_output,
            dim=1
        )


    # -------------------------------------------------
    # CLASS NAMES
    # -------------------------------------------------

    class_names = [
        "Low",
        "Medium",
        "High"
    ]


    # =================================================
    # JUNCTION RESULTS
    # =================================================

    junction_ids = [
        "402",
        "405",
        "219"
    ]

    junction_analysis = []


    for index, junction_id in enumerate(junction_ids):

        predicted_class = predictions[index].item()

        congestion = class_names[
            predicted_class
        ]

        confidence = (
            probabilities[index][predicted_class]
            .item() * 100
        )


        junction_analysis.append({

            "junction_id": junction_id,

            "congestion": congestion,

            "confidence": round(
                confidence,
                2
            )
        })


    # =================================================
    # CENTRAL JUNCTION
    # =================================================

    central_prediction = predictions[1].item()

    congestion = class_names[
        central_prediction
    ]


    # =================================================
    # TRAFFIC SCORE
    # =================================================

    traffic_score = (
        total_vehicles +
        (heavy * 2)
    )


    # =================================================
    # SIGNAL OPTIMIZATION
    # =================================================

    if congestion == "Low":

        green_time = 30
        red_time = 30

    elif congestion == "Medium":

        green_time = 45
        red_time = 30

    else:

        green_time = 60
        red_time = 20


    # =================================================
    # RETURN RESULT
    # =================================================

    return {

        "cars": cars,

        "heavy_vehicles": heavy,

        "total_vehicles": total_vehicles,

        "density": density,

        "traffic_score": traffic_score,

        "congestion": congestion,

        "green_time": green_time,

        "red_time": red_time,

        "model": "YOLO + GAT",

        "junction_analysis":
            junction_analysis
    }


# =====================================================
# DIRECT TEST
# =====================================================

if __name__ == "__main__":

    image_path = (
        "dataset/test_images/traffic1.jpg"
    )

    result = analyze_traffic(
        image_path
    )


    print("\n")

    print("=" * 60)

    print(
        "UrbanTwin AI - YOLO + GAT Traffic Pipeline"
    )

    print("=" * 60)


    print(
        f"Cars: {result['cars']}"
    )

    print(
        f"Heavy Vehicles: "
        f"{result['heavy_vehicles']}"
    )

    print(
        f"Total Vehicles: "
        f"{result['total_vehicles']}"
    )

    print(
        f"Traffic Density: "
        f"{result['density']}"
    )

    print(
        f"Traffic Score: "
        f"{result['traffic_score']}"
    )

    print(
        f"GAT Congestion: "
        f"{result['congestion']}"
    )

    print(
        f"Recommended Green Time: "
        f"{result['green_time']} seconds"
    )

    print(
        f"Recommended Red Time: "
        f"{result['red_time']} seconds"
    )

    print(
        f"Model: "
        f"{result['model']}"
    )


    print("\n")
    print("JUNCTION-WISE GAT ANALYSIS")
    print("-" * 60)


    for junction in result[
        "junction_analysis"
    ]:

        print(
            f"Junction "
            f"{junction['junction_id']} "
            f"→ "
            f"{junction['congestion']} "
            f"("
            f"{junction['confidence']}%"
            f")"
        )


    print("=" * 60)