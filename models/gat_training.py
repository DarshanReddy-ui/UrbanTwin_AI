import torch
import torch.nn as nn
import torch.optim as optim

from gat_model import GATModel


# ============================================================
# UrbanTwin AI - GAT Training
# ============================================================

print("=" * 60)
print("UrbanTwin AI - GAT Congestion Training")
print("=" * 60)


# ------------------------------------------------------------
# Training data
#
# Each row represents:
# [car_count, heavy_vehicle_count]
#
# Labels:
# 0 = Low
# 1 = Medium
# 2 = High
# ------------------------------------------------------------

training_data = [
    # Low traffic
    ([2, 0], 0),
    ([3, 0], 0),
    ([4, 0], 0),
    ([3, 1], 0),

    # Medium traffic
    ([5, 0], 1),
    ([6, 0], 1),
    ([5, 1], 1),
    ([7, 0], 1),
    ([6, 1], 1),

    # High traffic
    ([8, 0], 2),
    ([9, 0], 2),
    ([10, 1], 2),
    ([12, 1], 2),
    ([15, 2], 2),
]


# ------------------------------------------------------------
# Create graph
#
# Three connected junctions
# ------------------------------------------------------------

adjacency = torch.tensor(
    [
        [1.0, 1.0, 0.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0]
    ],
    dtype=torch.float32
)


# ------------------------------------------------------------
# Create GAT model
# ------------------------------------------------------------

model = GATModel(
    input_features=2,
    hidden_features=8,
    output_features=3
)


# ------------------------------------------------------------
# Loss function and optimizer
# ------------------------------------------------------------

criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=0.01
)


# ------------------------------------------------------------
# Training
# ------------------------------------------------------------

epochs = 300

print("\nStarting training...\n")


for epoch in range(epochs):

    total_loss = 0.0

    for features, label in training_data:

        # Convert one traffic condition into
        # three connected junctions.
        #
        # The same condition is used for this
        # small prototype training example.

        node_features = torch.tensor(
            [
                features,
                features,
                features
            ],
            dtype=torch.float32
        )

        target = torch.tensor(
            [label, label, label],
            dtype=torch.long
        )

        # Forward pass
        output = model(
            node_features,
            adjacency
        )

        # Calculate loss
        loss = criterion(
            output,
            target
        )

        # Clear old gradients
        optimizer.zero_grad()

        # Backpropagation
        loss.backward()

        # Update model
        optimizer.step()

        total_loss += loss.item()

    # Display progress
    if (epoch + 1) % 50 == 0:

        average_loss = total_loss / len(training_data)

        print(
            f"Epoch {epoch + 1:03d}/{epochs} "
            f"- Loss: {average_loss:.4f}"
        )


# ------------------------------------------------------------
# Save trained model
# ------------------------------------------------------------

model_path = "models/gat_traffic_model.pt"

torch.save(
    model.state_dict(),
    model_path
)


print("\nTraining completed successfully.")

print(
    f"Trained GAT model saved to: {model_path}"
)


# ------------------------------------------------------------
# Test the trained model
# ------------------------------------------------------------

print("\nTesting trained GAT...\n")


test_cases = [
    ([3, 0], "Expected: LOW"),
    ([6, 1], "Expected: MEDIUM"),
    ([12, 1], "Expected: HIGH")
]


class_names = [
    "LOW",
    "MEDIUM",
    "HIGH"
]


for features, expected in test_cases:

    node_features = torch.tensor(
        [
            features,
            features,
            features
        ],
        dtype=torch.float32
    )

    with torch.no_grad():

        output = model(
            node_features,
            adjacency
        )

        prediction = torch.argmax(
            output,
            dim=1
        )

    predicted_class = class_names[
        prediction[0].item()
    ]

    print(
        f"Traffic {features} "
        f"→ Predicted: {predicted_class} "
        f"({expected})"
    )


print("\nGAT training and testing completed.")
print("=" * 60)