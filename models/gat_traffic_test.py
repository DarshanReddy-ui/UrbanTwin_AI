import torch

from gat_model import GATModel
from traffic_graph import build_traffic_graph


print("=" * 60)
print("UrbanTwin AI - GAT Traffic Integration Test")
print("=" * 60)


# -------------------------------------------------
# STEP 1: Create traffic graph
# -------------------------------------------------

features, adjacency = build_traffic_graph(
    junction_402_cars=10,
    junction_402_heavy=1,
    junction_405_cars=8,
    junction_405_heavy=0,
    junction_219_cars=5,
    junction_219_heavy=1
)


print("\nTraffic Node Features:")
print(features)

print("\nTraffic Adjacency Matrix:")
print(adjacency)


# -------------------------------------------------
# STEP 2: Create GAT model
# -------------------------------------------------

model = GATModel(
    input_features=2,
    hidden_features=8,
    output_features=3
)


# -------------------------------------------------
# STEP 3: Send traffic graph into GAT
# -------------------------------------------------

with torch.no_grad():

    gat_output = model(
        features,
        adjacency
    )


# -------------------------------------------------
# STEP 4: Display GAT output
# -------------------------------------------------

print("\nGAT Traffic Output:")

print(gat_output)


# -------------------------------------------------
# STEP 5: Display output for each junction
# -------------------------------------------------

junctions = [
    "Junction 402",
    "Junction 405",
    "Junction 219"
]

print("\nJunction-wise GAT Output:")

for junction, output in zip(junctions, gat_output):

    print(
        f"{junction}: "
        f"{output.tolist()}"
    )


print("\nGAT traffic integration successful.")

print("=" * 60)