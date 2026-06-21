# Layer Normalization

## Overview
Layer Normalization is a technique used in artificial neural networks to normalize the inputs of a layer across the features, for each individual training example. Think of it as a way to standardize the data flowing through your network, but instead of doing it for the entire dataset at once (like traditional data scaling), or across a batch of samples (like Batch Normalization), it does it *per sample, per layer*.

Its primary goal is to stabilize the training process of deep neural networks, especially those with many layers or recurrent connections, leading to faster convergence and improved performance. It helps in making the network less sensitive to the initial weights and allows for higher learning rates. While Batch Normalization normalizes across the batch dimension, Layer Normalization normalizes across the feature dimension, making it particularly well-suited for architectures like Recurrent Neural Networks (RNNs) and Transformers, where batch statistics might be unstable or undefined (e.g., variable sequence lengths).

## What Problem It Solves
Layer Normalization addresses several critical challenges in training deep neural networks:

*   **Internal Covariate Shift (ICS)**: This is a phenomenon where the distribution of activations in hidden layers changes during training as the parameters of the preceding layers change. This continuous shift forces subsequent layers to constantly adapt to new input distributions, slowing down training and making it harder to converge. Layer Normalization mitigates ICS by stabilizing the input distribution to each layer, making the learning process smoother and more efficient.

*   **Vanishing and Exploding Gradients**: In deep networks, especially RNNs, gradients can become extremely small (vanish) or extremely large (explode) as they propagate through many layers. This makes it difficult for the network to learn long-term dependencies or update weights effectively. By normalizing activations, Layer Normalization keeps the scale of activations and gradients within a reasonable range, helping to prevent these issues and enabling deeper networks to train more effectively.

*   **Sensitivity to Initialization**: Deep neural networks are often very sensitive to the initial values of their weights. Poor initialization can lead to slow convergence or even prevent the network from learning at all. Normalization techniques like Layer Normalization make the network more robust to initialization choices by ensuring that activations remain within a stable range regardless of the initial weights.

*   **Limitations of Batch Normalization**: While Batch Normalization is highly effective, it has limitations:
    *   **Small Batch Sizes**: Batch Normalization relies on computing statistics (mean and variance) over a mini-batch. If the batch size is very small, these statistics become noisy and unreliable, leading to poor performance. Layer Normalization, by normalizing per sample, is completely independent of batch size.
    *   **Recurrent Neural Networks (RNNs)**: In RNNs, the input sequence length can vary, and applying Batch Normalization across the time dimension can be problematic. Also, the statistics for each time step might be different. Layer Normalization, by normalizing across features for each time step independently, is a natural fit for RNNs.
    *   **Generative Models (e.g., GANs)**: Some generative models require stable statistics across individual samples rather than batches.

## How It Works
Layer Normalization operates by normalizing the activations within a single layer, for each individual data sample. Let's break down the process step-by-step:

1.  **Input to a Layer**: Imagine you have a neural network layer (e.g., a fully connected layer or an LSTM cell). After the linear transformation (weights multiplied by inputs plus bias), but *before* the activation function, you get a vector of activations for each neuron in that layer. Let's call this vector $H$. For a single training example, $H$ is a vector where each element corresponds to the activation of a neuron in that layer.

2.  **Calculate Mean (Per Sample, Per Layer)**: For *each individual training example*, Layer Normalization calculates the mean of all the activations within that specific layer. So, if a layer has $M$ neurons, it computes the average of these $M$ activation values for that one sample. This is different from Batch Normalization, which calculates the mean of a *single neuron's activation* across all samples in a batch.

3.  **Calculate Variance (Per Sample, Per Layer)**: Similarly, for *each individual training example*, Layer Normalization calculates the variance of all the activations within that same layer. This measures how spread out the activations are for that sample across the layer's neurons.

4.  **Normalize**: Using the calculated mean and variance, each activation in the layer for that sample is then normalized. This involves subtracting the mean and dividing by the standard deviation (square root of variance). This process transforms the activations such that they have a mean of 0 and a standard deviation of 1. A small constant $\epsilon$ (epsilon) is added to the variance before taking the square root to prevent division by zero in cases where the variance might be extremely small.

5.  **Scale and Shift (Learnable Parameters)**: After normalization, Layer Normalization introduces two learnable parameters:
    *   **Gamma ($\gamma$)**: A scaling factor.
    *   **Beta ($\beta$)**: A shifting factor (bias).
    These parameters allow the network to learn an optimal mean and variance for the normalized activations, rather than being forced into a strict mean of 0 and standard deviation of 1. This preserves the representational power of the network, as sometimes a non-zero mean or non-unit variance might be optimal for the subsequent layers. These $\gamma$ and $\beta$ parameters are learned during the backpropagation process, just like other weights and biases in the network.

Crucially, because Layer Normalization computes statistics *per sample*, it behaves identically during training and inference. There's no need to maintain running averages of statistics, unlike Batch Normalization.

## Mathematical Intuition

Let's denote the input to a layer for a single training example as a vector $x = [x_1, x_2, \dots, x_M]$, where $M$ is the number of features (or neurons) in that layer.

For this single input $x$, Layer Normalization performs the following steps:

1.  **Calculate the Mean ($\mu$)**: The mean of the activations across all $M$ features for this specific sample is calculated:
    $$\mu = \frac{1}{M} \sum_{i=1}^{M} x_i$$
    Here, $x_i$ represents the activation of the $i$-th neuron in the layer for the current sample.

2.  **Calculate the Variance ($\sigma^2$)**: The variance of the activations across all $M$ features for this specific sample is calculated:
    $$\sigma^2 = \frac{1}{M} \sum_{i=1}^{M} (x_i - \mu)^2$$

3.  **Normalize the Activations ($\hat{x}_i$)**: Each individual activation $x_i$ is then normalized using the calculated mean and variance:
    $$\hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}}$$
    Here, $\epsilon$ is a small constant (e.g., $10^{-5}$ or $10^{-9}$) added to the variance to prevent division by zero, especially if the variance is very small.

4.  **Apply Learnable Scale ($\gamma$) and Shift ($\beta$)**: Finally, the normalized activation $\hat{x}_i$ is scaled by a learnable parameter $\gamma$ and shifted by a learnable parameter $\beta$. These parameters are unique to each layer and are learned during training via backpropagation.
    $$y_i = \gamma \hat{x}_i + \beta$$
    The output $y_i$ is the final normalized, scaled, and shifted activation that will be passed to the activation function of the layer or to the next layer.

**Key takeaway**: The mean $\mu$ and variance $\sigma^2$ are computed *independently for each sample* and *across all features within that sample's layer*. This is the fundamental difference from Batch Normalization, where $\mu$ and $\sigma^2$ are computed *across the batch dimension* for each feature independently.

## Advantages
*   **Independent of Batch Size**: Layer Normalization computes statistics (mean and variance) for each individual sample, making it robust to varying batch sizes, including batch size 1. This is crucial for online learning, reinforcement learning, and when memory constraints limit batch size.
*   **Effective for RNNs and Transformers**: It is particularly well-suited for models that process sequential data (like RNNs, LSTMs, GRUs) and attention-based models (like Transformers). In these architectures, sequence lengths can vary, and batch statistics can be unstable. Layer Normalization normalizes across the feature dimension at each time step, which is a natural fit.
*   **Stabilizes Hidden State Dynamics**: By normalizing activations, it helps in stabilizing the distribution of hidden states, preventing vanishing or exploding gradients, and allowing for deeper and more complex models to be trained.
*   **Faster Convergence**: By reducing internal covariate shift and stabilizing gradients, Layer Normalization often leads to faster training convergence and allows for the use of higher learning rates.
*   **No Training/Inference Mode Difference**: Unlike Batch Normalization, Layer Normalization behaves identically during training and inference because it doesn't rely on batch statistics or running averages. This simplifies deployment and avoids potential discrepancies.
*   **Reduces Sensitivity to Initialization**: It makes the network less dependent on careful weight initialization, allowing for more robust training.

## Disadvantages
*   **May Not Always Outperform Batch Normalization on CNNs**: While Layer Normalization is excellent for sequence models, Batch Normalization often still holds an edge in traditional Convolutional Neural Networks (CNNs) for image tasks, especially with large batch sizes. This is because Batch Normalization normalizes across the batch, which can be beneficial for learning feature representations that are consistent across different images.
*   **Computational Overhead**: While generally minor, Layer Normalization does add a small computational cost per layer due to the mean and variance calculations and the scaling/shifting operations. However, this is usually outweighed by the benefits of faster convergence.
*   **Less Effective for Very Shallow Networks**: In very shallow networks, the benefits of normalization might be less pronounced, and the added complexity might not be justified.
*   **Can Obscure Feature Importance (Rare)**: In some niche cases, normalizing across all features within a layer might theoretically obscure the relative importance of certain features if their natural scale differences carry significant information. However, the learnable $\gamma$ and $\beta$ parameters usually mitigate this by allowing the network to re-scale and re-shift as needed.

## Real World Applications
Layer Normalization has become a cornerstone technique in various state-of-the-art machine learning models and is widely applied across different domains:

1.  **Natural Language Processing (NLP)**: This is arguably where Layer Normalization has had its most significant impact. It is a fundamental component of the Transformer architecture, which powers models like BERT, GPT (GPT-2, GPT-3, GPT-4), T5, and many other large language models. In Transformers, Layer Normalization is typically applied after the multi-head attention and feed-forward sub-layers, helping to stabilize the training of these very deep and complex models.
2.  **Recurrent Neural Networks (RNNs)**: Before the rise of Transformers, Layer Normalization was widely adopted in RNN variants like LSTMs and GRUs. It helps stabilize the hidden states over long sequences, mitigating vanishing/exploding gradients and improving the ability of RNNs to learn long-term dependencies in tasks like machine translation, speech recognition, and sentiment analysis.
3.  **Speech Recognition**: Deep learning models for speech recognition, which often involve complex recurrent or attention-based architectures, heavily utilize Layer Normalization to handle variable-length audio sequences and stabilize training.
4.  **Reinforcement Learning**: In some reinforcement learning setups, especially those involving deep policy networks or value networks, Layer Normalization can be used to stabilize the training of these networks, particularly when dealing with diverse or changing input states.
5.  **Generative Adversarial Networks (GANs)**: While Batch Normalization is more common in GANs, Layer Normalization is sometimes used, especially in specific architectures or when dealing with very small batch sizes where Batch Normalization might fail. It can help stabilize the training of both the generator and discriminator networks.

## Python Example

This example demonstrates Layer Normalization using PyTorch, a popular deep learning framework. We'll create a dummy tensor representing a batch of sequences (e.g., from an NLP task) and apply `torch.nn.LayerNorm` to it.

```python
import torch
import torch.nn as nn
import numpy as np

# --- 1. Generate Dummy Data ---
# Let's simulate an input tensor for a Transformer or RNN.
# Dimensions: (batch_size, sequence_length, embedding_dim)
# batch_size: Number of independent samples in the batch
# sequence_length: Number of tokens/time steps in each sequence
# embedding_dim: Number of features for each token/time step (e.g., 512, 768)

batch_size = 4
sequence_length = 10
embedding_dim = 6

# Create a random tensor with values that are not normalized
# Using torch.randn for random values from a standard normal distribution
# Then multiplying by 10 and adding 5 to make them clearly non-normalized
input_data = torch.randn(batch_size, sequence_length, embedding_dim) * 10 + 5
print("Original Input Data Shape:", input_data.shape)
print("Original Input Data (first sample, first token):\n", input_data[0, 0])
print("Original Input Data Mean (first sample, first token):", input_data[0, 0].mean().item())
print("Original Input Data Std (first sample, first token):", input_data[0, 0].std().item())
print("-" * 50)

# --- 2. Instantiate Layer Normalization Layer ---
# LayerNorm expects the 'normalized_shape' argument.
# This specifies the dimensions over which to compute the mean and variance.
# If input is (B, S, E), and we want to normalize across 'E' (embedding_dim),
# then normalized_shape should be (E,).
# If we wanted to normalize across (S, E), it would be (S, E).
# In Transformers, it's typically applied to the last dimension (feature dimension).
layer_norm = nn.LayerNorm(normalized_shape=embedding_dim)

# The LayerNorm layer also has learnable parameters gamma (weight) and beta (bias).
# Let's inspect them before applying.
print("LayerNorm Learnable Weight (gamma) before training:", layer_norm.weight.data)
print("LayerNorm Learnable Bias (beta) before training:", layer_norm.bias.data)
print("-" * 50)

# --- 3. Apply Layer Normalization ---
normalized_output = layer_norm(input_data)

print("Normalized Output Data Shape:", normalized_output.shape)
print("Normalized Output Data (first sample, first token):\n", normalized_output[0, 0])

# --- 4. Verify Normalization (Mean and Standard Deviation) ---
# For Layer Normalization, the mean and std are calculated PER SAMPLE, PER LAYER.
# Let's check the mean and std for the first sample's first token's features.
# This should be close to 0 and 1 respectively.
print("\nVerification:")
print("Mean of normalized features for first sample, first token:", normalized_output[0, 0].mean().item())
print("Std of normalized features for first sample, first token:", normalized_output[0, 0].std().item())

# Let's check for another sample and token to confirm it's per-sample
print("Mean of normalized features for second sample, third token:", normalized_output[1, 2].mean().item())
print("Std of normalized features for second sample, third token:", normalized_output[1, 2].std().item())

# You can also manually calculate to confirm
# For the first sample, first token:
manual_mean = input_data[0, 0].mean()
manual_std = input_data[0, 0].std()
epsilon = layer_norm.eps # Get the epsilon used by the LayerNorm layer
manual_normalized = (input_data[0, 0] - manual_mean) / torch.sqrt(manual_std**2 + epsilon)
# After normalization, apply gamma and beta (which are initialized to 1 and 0 respectively)
manual_output = layer_norm.weight * manual_normalized + layer_norm.bias

print("\nManual verification for first sample, first token:")
print("Manually calculated normalized output:\n", manual_output)
print("Difference from PyTorch output (should be very small):\n", (manual_output - normalized_output[0, 0]).abs().sum().item())

print("-" * 50)

# --- 5. Demonstrate Independence from Batch Size ---
# Even if we pass a single sample, LayerNorm works the same way.
single_sample_input = input_data[0:1, :, :] # Take only the first sample
single_sample_output = layer_norm(single_sample_input)

print("Single Sample Input Shape:", single_sample_input.shape)
print("Single Sample Normalized Output Shape:", single_sample_output.shape)
print("Mean of normalized features for single sample, first token:", single_sample_output[0, 0].mean().item())
print("Std of normalized features for single sample, first token:", single_sample_output[0, 0].std().item())
```

**Explanation of the Code:**

1.  **Dummy Data**: We create a 3D tensor `input_data` with dimensions `(batch_size, sequence_length, embedding_dim)`. This is a common shape for inputs to Transformer encoder/decoder layers or RNNs. The values are intentionally made non-normalized to clearly show the effect of Layer Normalization.
2.  **`nn.LayerNorm`**: We instantiate `nn.LayerNorm`. The `normalized_shape` argument is crucial. Here, `embedding_dim` (which is 6) tells LayerNorm to compute the mean and variance across the *last dimension* (the feature dimension) for each individual `(batch_item, sequence_item)` combination.
3.  **Apply LayerNorm**: We simply pass our `input_data` through the `layer_norm` instance.
4.  **Verification**: We then print the mean and standard deviation of the normalized output for specific tokens. You'll observe that these values are very close to 0 and 1, respectively, confirming that the normalization has occurred *per sample, per layer (or per token in this case)*. The manual calculation further confirms the process.
5.  **Batch Size Independence**: We demonstrate that Layer Normalization works perfectly fine even with a batch size of 1, producing consistent normalized outputs, unlike Batch Normalization which would struggle with such small batches.

## Interview Questions

1.  **What is Layer Normalization and what is its primary purpose?**
    *   **Answer**: Layer Normalization is a technique to normalize the inputs of a layer across the features, for each individual training example. Its primary purpose is to stabilize the training of deep neural networks, accelerate convergence, and mitigate issues like internal covariate shift and vanishing/exploding gradients, especially in architectures like RNNs and Transformers.

2.  **How does Layer Normalization differ from Batch Normalization?**
    *   **Answer**: The key difference lies in *which dimension* the statistics (mean and variance) are computed over.
        *   **Batch Normalization**: Computes mean and variance *across the batch dimension* for each feature independently. It normalizes features `j` using statistics from all samples in the batch for feature `j`.
        *   **Layer Normalization**: Computes mean and variance *across the feature dimension* for each individual sample independently. It normalizes sample `i` using statistics from all features in sample `i`.

3.  **When would you prefer Layer Normalization over Batch Normalization?**
    *   **Answer**: Layer Normalization is preferred in scenarios where:
        *   **Small Batch Sizes**: Batch Normalization performs poorly with small batches due to noisy statistics. Layer Normalization is independent of batch size.
        *   **Recurrent Neural Networks (RNNs)**: RNNs often have variable sequence lengths, and batch statistics can be unstable across time steps. Layer Normalization normalizes each time step's features independently.
        *   **Transformer Architectures**: It's the standard normalization technique in Transformers (e.g., BERT, GPT) due to its stability and independence from sequence length and batch size.
        *   **Online Learning/Reinforcement Learning**: Where batch statistics might not be available or are constantly changing.

4.  **Explain the role of $\gamma$ (gamma) and $\beta$ (beta) in Layer Normalization.**
    *   **Answer**: After the raw normalization (mean 0, std 1), Layer Normalization applies two learnable parameters:
        *   **$\gamma$ (gamma)**: A scaling factor. It allows the network to learn to scale the normalized activations up or down.
        *   **$\beta$ (beta)**: A shifting factor (bias). It allows the network to learn to shift the mean of the normalized activations.
        These parameters restore the representational power of the network, allowing it to learn an optimal mean and variance for the activations, rather than being strictly constrained to 0 and 1. They are learned during backpropagation.

5.  **Does Layer Normalization have different behavior during training and inference?**
    *   **Answer**: No, Layer Normalization behaves identically during training and inference. Since it computes the mean and variance *per sample* (not across a batch), there's no need to maintain running averages of statistics or switch between training and inference modes, simplifying deployment.

6.  **How does Layer Normalization help with vanishing/exploding gradients?**
    *   **Answer**: By normalizing the activations within each layer to have a stable mean and variance, Layer Normalization helps keep the scale of activations and gradients within a reasonable range. This prevents gradients from becoming excessively small (vanishing) or excessively large (exploding) as they propagate through many layers, thus enabling more stable and effective training of deep networks.

7.  **Can Layer Normalization be applied to convolutional layers? If so, how?**
    *   **Answer**: Yes, Layer Normalization can be applied to convolutional layers. When applied to a convolutional layer's output, it typically normalizes across the channel and spatial dimensions for each individual sample. For an output tensor of shape `(N, C, H, W)` (Batch, Channels, Height, Width), Layer Normalization would compute mean and variance over `C * H * W` elements for each of the `N` samples. While less common than Batch Normalization in traditional CNNs, it is used in some architectures, especially those that are sensitive to batch size.

8.  **What is "Internal Covariate Shift" and how does Layer Normalization address it?**
    *   **Answer**: Internal Covariate Shift (ICS) refers to the phenomenon where the distribution of activations in hidden layers changes during training as the parameters of the preceding layers are updated. This continuous shift forces subsequent layers to constantly adapt to new input distributions, slowing down training. Layer Normalization addresses ICS by stabilizing the input distribution to each layer. By normalizing the activations to have a consistent mean and variance (which can then be scaled and shifted by $\gamma$ and $\beta$), it ensures that each layer receives inputs with a more stable distribution, making the learning process smoother and more efficient.

9.  **What are the computational costs of Layer Normalization compared to Batch Normalization?**
    *   **Answer**: Both Layer Normalization and Batch Normalization introduce a small computational overhead per layer. Layer Normalization involves calculating mean and variance for each sample across its features, which is typically a vector operation. Batch Normalization calculates mean and variance for each feature across the batch. In practice, the computational cost is usually negligible compared to the matrix multiplications in deep layers, and the benefits of faster convergence often outweigh this minor overhead for both techniques.

10. **In what specific deep learning architectures is Layer Normalization particularly effective, and why?**
    *   **Answer**: Layer Normalization is particularly effective in:
        *   **Transformers**: It's a core component, applied after multi-head attention and feed-forward sub-layers. It stabilizes the training of these very deep, self-attentive networks, which are crucial for NLP tasks.
        *   **Recurrent Neural Networks (RNNs), LSTMs, GRUs**: It helps stabilize hidden states over long sequences and across variable sequence lengths, mitigating vanishing/exploding gradients, which are common issues in RNNs.
        *   **Generative Models (sometimes)**: In cases where batch statistics are unreliable or when specific architectural choices benefit from per-sample normalization.
    The effectiveness stems from its independence from batch size and its ability to normalize across the feature dimension, which aligns well with the data flow in these architectures.

## Quiz

1.  Which of the following best describes how Layer Normalization computes its statistics (mean and variance)?
    A) Across the batch dimension for each feature independently.
    B) Across the feature dimension for each individual sample independently.
    C) Across all features and all samples in the entire dataset.
    D) Only during inference, using pre-computed statistics from training.

2.  What is a primary advantage of Layer Normalization over Batch Normalization, especially in RNNs and Transformers?
    A) It requires less memory during training.
    B) It has a different behavior during training and inference, allowing for specialized optimization.
    C) It is independent of batch size, making it robust to small or varying batch sizes.
    D) It completely eliminates the need for activation functions.

3.  The learnable parameters $\gamma$ (gamma) and $\beta$ (beta) in Layer Normalization serve what purpose?
    A) To determine the learning rate for the layer.
    B) To scale and shift the normalized activations, allowing the network to learn an optimal distribution.
    C) To introduce non-linearity into the normalization process.
    D) To regularize the weights of the layer, preventing overfitting.

4.  Layer Normalization is particularly effective in mitigating which of the following problems?
    A) Overfitting to the training data.
    B) Internal Covariate Shift and vanishing/exploding gradients.
    C) Slow computation of forward passes.
    D) The need for a GPU for training.

5.  If an input tensor to a Layer Normalization layer has the shape `(Batch_Size, Sequence_Length, Embedding_Dimension)`, and we want to normalize across the `Embedding_Dimension` for each `(Batch_Size, Sequence_Length)` element, what should be the `normalized_shape` argument for `torch.nn.LayerNorm`?
    A) `(Batch_Size,)`
    B) `(Sequence_Length,)`
    C) `(Embedding_Dimension,)`
    D) `(Batch_Size, Sequence_Length, Embedding_Dimension)`

---

### Answer Key

1.  **B) Across the feature dimension for each individual sample independently.**
    *   **Explanation**: This is the defining characteristic of Layer Normalization. It normalizes each sample's features within a layer, making it independent of other samples in the batch.

2.  **C) It is independent of batch size, making it robust to small or varying batch sizes.**
    *   **Explanation**: Batch Normalization struggles with small batch sizes because its statistics become unreliable. Layer Normalization's per-sample computation makes it immune to this issue, which is crucial for RNNs (variable sequence lengths) and Transformers (often trained with small effective batch sizes or on single samples).

3.  **B) To scale and shift the normalized activations, allowing the network to learn an optimal distribution.**
    *   **Explanation**: After normalizing to mean 0 and std 1, $\gamma$ and $\beta$ allow the network to "undo" or adjust this strict normalization if a different mean and variance are more optimal for the learning task, preserving the model's representational capacity.

4.  **B) Internal Covariate Shift and vanishing/exploding gradients.**
    *   **Explanation**: By stabilizing the distribution of layer inputs and outputs, Layer Normalization directly addresses Internal Covariate Shift and helps keep gradients within a manageable range, preventing them from vanishing or exploding.

5.  **C) `(Embedding_Dimension,)`**
    *   **Explanation**: The `normalized_shape` argument specifies the dimensions over which the mean and variance are computed. If you want to normalize across the `Embedding_Dimension` for each `(Batch_Size, Sequence_Length)` element, you specify the shape of the dimensions you want to normalize over, which is just `Embedding_Dimension` in this case.

## Further Reading

1.  **Original Paper**: [Layer Normalization](https://arxiv.org/abs/1607.06450) by Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E. Hinton (2016). This is the foundational paper introducing the concept.
2.  **PyTorch Documentation**: [torch.nn.LayerNorm](https://pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html). Official documentation providing details on its implementation and usage in PyTorch.
3.  **TensorFlow Documentation**: [tf.keras.layers.LayerNormalization](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LayerNormalization). Official documentation for TensorFlow's Keras implementation.
4.  **Blog Post/Tutorial**: Many excellent blog posts explain Layer Normalization in detail, often comparing it with Batch Normalization. Searching for "Layer Normalization explained" will yield many good resources, such as articles on Towards Data Science or Analytics Vidhya.