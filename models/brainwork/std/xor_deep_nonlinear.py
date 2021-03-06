import numpy as np
from ...utilities.activations import relu, drelu

# Inputs
train_lights = np.array([
    [1, 0, 0, 1],
    [0, 1, 0, 1],
])

# Weights
weights_0_1 = np.random.randn(2, 2)
weights_1_2 = np.random.randn(1, 2)

# Initial Weights
weights_0_1_init = weights_0_1.copy()
weights_1_2_init = weights_1_2.copy()

# Labels
walk_or_stop = np.array([0, 0, 0, 10])

# Parameters
alpha = 0.0001

# Train
for i in range(int(1e5)):
    # Forward Layers
    layer_0 = train_lights
    layer_1 = relu(weights_0_1.dot(layer_0))
    layer_2 = weights_1_2.dot(layer_1)

    # Error
    layer_2_delta = layer_2 - walk_or_stop
    layer_1_delta = weights_1_2.T.dot(layer_2_delta) * drelu(layer_1)

    error = np.linalg.norm(layer_2_delta) + np.linalg.norm(layer_1_delta)

    # Gradient
    weights_1_2_gradient = layer_2_delta.dot(layer_1.T)
    weights_0_1_gradient = layer_1_delta.dot(layer_0.T)

    # Descent
    weights_1_2 -= alpha * weights_1_2_gradient
    weights_0_1 -= alpha * weights_0_1_gradient

    if not i % 1000:
        print(error)
