import string
import numpy as np

# Load Data
with open("./data/bible.txt") as fs:
    without_punctuation = str.maketrans('', '', string.punctuation)

    corpus = fs.read().lower().translate(without_punctuation).split()

    vocab = {}
    identity = 0
    for word in corpus:
        if word not in vocab:
            vocab[word] = identity
            identity += 1

# Hyperparameters
alpha = 0.0001
iterations = int(1e0)
window_size = 3
embedding_size = 40

weights_0_1_dims = (len(vocab), embedding_size)
weights_1_2_dims = (embedding_size, len(vocab))

# Weights
weights_0_1 = np.random.randn(*weights_0_1_dims)
weights_1_2 = np.random.randn(*weights_1_2_dims)

# Training
sample = corpus[:16]

for iteration in range(iterations):
    for si in range(window_size, len(sample) - window_size + 1):
        window = sample[si-window_size: si+window_size]

        input_word, target_word = np.random.choice(window,
                                                   size=2,
                                                   replace=False)

        layer_0 = vocab[input_word]
        layer_1 = weights_0_1[layer_0]  # Embedding Layer
        layer_2 = layer_1.dot(weights_1_2)

        target_layer = np.zeros(len(vocab))
        target_layer[vocab[target_word]] = 10

        layer_2_delta = target_layer - layer_2
        layer_1_delta = layer_2_delta.reshape(1, -1).dot(weights_1_2.T)

        weights_1_2_grad = layer_1.reshape(1, -1).T.dot(layer_2_delta.reshape(1, -1))
        weights_0_1_grad = layer_1_delta.reshape(-1)

        weights_1_2 -= alpha * weights_1_2_grad
        weights_0_1[layer_0] -= alpha * weights_0_1_grad
    
    if not iteration % 10:
        print(np.square(target_layer - layer_2).sum())