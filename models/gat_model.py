import torch
import torch.nn as nn
import torch.nn.functional as F


class GraphAttentionLayer(nn.Module):
    """
    Basic Graph Attention Layer.

    Each traffic junction receives information from
    connected junctions and assigns attention weights
    to their features.
    """

    def __init__(self, in_features, out_features):
        super().__init__()

        self.in_features = in_features
        self.out_features = out_features

        # Linear transformation of node features
        self.W = nn.Linear(in_features, out_features, bias=False)

        # Attention parameters
        self.a = nn.Linear(out_features * 2, 1, bias=False)

    def forward(self, x, adjacency):
        """
        x:
            Node feature matrix
            Shape: [number_of_nodes, input_features]

        adjacency:
            Graph adjacency matrix
            Shape: [number_of_nodes, number_of_nodes]
        """

        # Transform node features
        h = self.W(x)

        number_of_nodes = h.size(0)

        # Prepare pairs of nodes
        h_i = h.repeat_interleave(number_of_nodes, dim=0)
        h_j = h.repeat(number_of_nodes, 1)

        # Combine neighboring node features
        pair_features = torch.cat([h_i, h_j], dim=1)

        # Calculate attention scores
        attention_scores = self.a(pair_features)
        attention_scores = attention_scores.view(
            number_of_nodes,
            number_of_nodes
        )

        # LeakyReLU activation
        attention_scores = F.leaky_relu(
            attention_scores,
            negative_slope=0.2
        )

        # Only allow connected nodes to communicate
        mask = adjacency == 0

        attention_scores = attention_scores.masked_fill(
            mask,
            -9e15
        )

        # Normalize attention values
        attention_weights = F.softmax(
            attention_scores,
            dim=1
        )

        # Aggregate neighboring features
        output = torch.matmul(
            attention_weights,
            h
        )

        return output


class GATModel(nn.Module):
    """
    Graph Attention Network for traffic congestion analysis.
    """

    def __init__(
        self,
        input_features=2,
        hidden_features=8,
        output_features=3
    ):
        super().__init__()

        self.gat1 = GraphAttentionLayer(
            input_features,
            hidden_features
        )

        self.gat2 = GraphAttentionLayer(
            hidden_features,
            output_features
        )

    def forward(self, x, adjacency):

        x = self.gat1(x, adjacency)

        x = F.elu(x)

        x = self.gat2(x, adjacency)

        return x


def create_traffic_graph():

    """
    Creates a simple traffic graph representing
    three connected traffic junctions.

    Junctions:
        402
        405
        219
    """

    # Node features:
    # [vehicle_count, heavy_vehicle_count]

    x = torch.tensor(
        [
            [10.0, 1.0],   # Junction 402
            [8.0, 0.0],    # Junction 405
            [5.0, 1.0]     # Junction 219
        ]
    )

    # Graph connections
    adjacency = torch.tensor(
        [
            [1.0, 1.0, 0.0],
            [1.0, 1.0, 1.0],
            [0.0, 1.0, 1.0]
        ]
    )

    return x, adjacency


if __name__ == "__main__":

    print("=" * 50)
    print("UrbanTwin AI - GAT Model Test")
    print("=" * 50)

    # Create traffic graph
    features, adjacency = create_traffic_graph()

    print("\nTraffic Node Features:")
    print(features)

    print("\nTraffic Graph:")
    print(adjacency)

    # Create GAT model
    model = GATModel()

    # Run model
    output = model(
        features,
        adjacency
    )

    print("\nGAT Output:")
    print(output)

    print("\nGAT model executed successfully.")
    print("=" * 50)