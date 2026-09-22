import torch


def build_traffic_graph(
    junction_402_cars,
    junction_402_heavy,
    junction_405_cars,
    junction_405_heavy,
    junction_219_cars,
    junction_219_heavy
):
    """
    Creates a traffic graph using vehicle counts
    from three connected junctions.

    Each junction is represented by:
    [car_count, heavy_vehicle_count]
    """

    node_features = torch.tensor(
        [
            [junction_402_cars, junction_402_heavy],
            [junction_405_cars, junction_405_heavy],
            [junction_219_cars, junction_219_heavy]
        ],
        dtype=torch.float32
    )

    # Traffic network connections
    #
    # 402 <----> 405 <----> 219
    #
    adjacency = torch.tensor(
        [
            [1.0, 1.0, 0.0],
            [1.0, 1.0, 1.0],
            [0.0, 1.0, 1.0]
        ],
        dtype=torch.float32
    )

    return node_features, adjacency


if __name__ == "__main__":

    print("=" * 55)
    print("UrbanTwin AI - Traffic Graph Builder Test")
    print("=" * 55)

    # Example traffic values
    features, adjacency = build_traffic_graph(
        junction_402_cars=10,
        junction_402_heavy=1,
        junction_405_cars=8,
        junction_405_heavy=0,
        junction_219_cars=5,
        junction_219_heavy=1
    )

    print("\nNode Features:")
    print(features)

    print("\nAdjacency Matrix:")
    print(adjacency)

    print("\nTraffic graph created successfully.")
    print("=" * 55)