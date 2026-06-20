# Cosine Annealing

## Overview
Cosine Annealing is a learning rate scheduling technique used in training deep neural networks. In machine learning, the "learning rate" is a hyperparameter that determines the step size at each iteration while moving toward a minimum of the loss function. A carefully chosen learning rate is crucial for efficient training; too high, and the model might overshoot the minimum; too low, and training can be excessively slow or get stuck in a suboptimal local minimum.

Cosine Annealing, often associated with "Stochastic Gradient Descent with Warm Restarts" (SGDR), proposes a learning rate schedule that periodically decreases the learning rate following a cosine curve and then "restarts" it to a higher value. This cyclical behavior helps the model explore different parts of the loss landscape, escape local minima, and potentially converge to better, flatter minima, leading to improved generalization performance. It's a dynamic approach that contrasts with static or monotonically decreasing learning rate schedules.

## What Problem It Solves
Cosine Annealing primarily addresses several challenges encountered during the training of deep neural networks:

1.  **Getting Stuck in Suboptimal Local Minima:** Traditional learning rate schedules often monotonically decrease the learning rate over time. While this helps fine-tune the model as it approaches a minimum, it can also cause the optimization process to get trapped in a suboptimal local minimum. With a very small learning rate, the model lacks the "energy" to jump out of such a minimum, even if a better one exists nearby.

2.  **Slow Convergence with Small Learning Rates:** If the learning rate is too small from the beginning, the training process can be extremely slow, requiring many more iterations to converge.

3.  **Overshooting with Large Learning Rates:** Conversely, if the learning rate is too large, the optimizer might repeatedly overshoot the minimum, causing the loss to oscillate wildly or even diverge.

4.  **Lack of Exploration:** Monotonically decreasing learning rates reduce the model's ability to explore the loss landscape. Once the learning rate becomes very small, the model essentially "settles" into a specific region. This can prevent it from discovering flatter, wider minima that often correspond to better generalization performance.

Cosine Annealing, especially with warm restarts, tackles these issues by:
*   **Periodically increasing the learning rate:** The "warm restart" mechanism periodically resets the learning rate to a higher value. This provides the optimizer with renewed "momentum" to jump out of potential local minima and explore new regions of the loss landscape.
*   **Smooth, controlled decay:** The cosine-shaped decay ensures a smooth and gradual reduction of the learning rate within each cycle, allowing for fine-tuning as the model approaches a minimum, but without getting stuck indefinitely.
*   **Finding Flatter Minima:** The cyclical nature encourages the model to visit multiple minima. Research suggests that flatter minima often generalize better than sharp ones. By periodically "bouncing out" of sharp minima, the model is more likely to settle in flatter regions.

## How It Works
Cosine Annealing, particularly in its "warm restarts" variant (SGDR), operates in cycles. Here's a step-by-step breakdown:

1.  **Define Cycle Length ($T_i$):** You start by defining an initial cycle length, $T_0$, which is the number of epochs (or batches) over which the learning rate will decay from its maximum to its minimum.

2.  **Learning Rate Decay (Cosine Curve):** Within each cycle, the learning rate starts at a maximum value ($\eta_{max}$) and gradually decreases to a minimum value ($\eta_{min}$) following a cosine function. The decay is not linear; it's faster at the beginning and end of the cycle and slower in the middle. This smooth decay allows the model to make larger updates initially and then fine-tune as it approaches a potential minimum.

3.  **Warm Restart:** At the end of each cycle (i.e., after $T_i$ epochs), the learning rate is "restarted" or reset back to its initial maximum value ($\eta_{max}$). This sudden jump in the learning rate provides the "warm restart" effect, giving the optimizer a fresh burst of energy to potentially escape a local minimum it might have settled into.

4.  **Increasing Cycle Length (Optional but Common):** A common practice with warm restarts is to increase the length of subsequent cycles. For example, the second cycle might be $T_1 = T_0 \times 2$ epochs long, the third $T_2 = T_1 \times 2$ epochs, and so on. This means the model spends progressively more time exploring and fine-tuning within each cycle before the next restart. This allows for broader exploration in earlier cycles and more refined convergence in later, longer cycles.

5.  **Repeat:** Steps 2-4 are repeated for the entire training duration. The model goes through multiple cycles of learning rate decay and warm restarts.

**Analogy:** Imagine searching for the lowest point in a hilly landscape while blindfolded.
*   **High Learning Rate:** You take big steps, covering ground quickly.
*   **Low Learning Rate:** You take small steps, carefully exploring the immediate area.
*   **Monotonic Decay:** You start with big steps, then gradually take smaller and smaller steps. You might get stuck in the first valley you find.
*   **Cosine Annealing with Warm Restarts:** You start with big steps, then gradually take smaller steps to explore a valley. Once you've explored it, you suddenly take a big jump (restart) to a new, potentially higher, starting point to explore a completely different region. Then you repeat, gradually taking smaller steps in this new region, and so on. This strategy increases your chances of finding the absolute lowest point (global minimum) or a very good one.

## Mathematical Intuition
The core of Cosine Annealing lies in the cosine function, which provides a smooth, non-linear decay. The most common formulation, as introduced in the SGDR paper, is:

$$ \eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})\left(1 + \cos\left(\frac{T_{cur}}{T_i}\pi\right)\right) $$

Let's break down each component:

*   $\eta_t$: This is the learning rate at a given time step (or epoch) $t$.
*   $\eta_{min}$: This is the minimum learning rate allowed within a cycle. The learning rate will never go below this value.
*   $\eta_{max}$: This is the maximum learning rate allowed within a cycle. The learning rate starts at this value at the beginning of each cycle.
*   $T_{cur}$: This represents the number of epochs (or batches) that have passed since the last restart. It effectively tracks the current position within the current cycle. $T_{cur}$ starts at 0 at the beginning of each cycle and increments up to $T_i - 1$.
*   $T_i$: This is the total number of epochs (or batches) in the current cycle. This value can be fixed or increased after each restart (e.g., $T_{i+1} = T_i \times \text{factor}$).
*   $\pi$: The mathematical constant pi, approximately 3.14159.

**How the cosine part works:**
The term $\cos\left(\frac{T_{cur}}{T_i}\pi\right)$ is the heart of the decay.
*   When $T_{cur} = 0$ (start of a cycle), the term becomes $\cos(0) = 1$.
*   When $T_{cur} = T_i$ (end of a cycle), the term becomes $\cos(\pi) = -1$.

So, as $T_{cur}$ goes from $0$ to $T_i$, the value of $\cos\left(\frac{T_{cur}}{T_i}\pi\right)$ smoothly goes from $1$ to $-1$.

Now, let's substitute these values back into the full equation:

1.  **At the beginning of a cycle ($T_{cur} = 0$):**
    $$ \eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})(1 + 1) $$
    $$ \eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})(2) $$
    $$ \eta_t = \eta_{min} + (\eta_{max} - \eta_{min}) $$
    $$ \eta_t = \eta_{max} $$
    The learning rate starts at its maximum value.

2.  **At the end of a cycle ($T_{cur} = T_i$):**
    $$ \eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})(1 + (-1)) $$
    $$ \eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})(0) $$
    $$ \eta_t = \eta_{min} $$
    The learning rate ends at its minimum value.

The term $\frac{1}{2}(\eta_{max} - \eta_{min})$ scales the cosine wave, and the $1 + \dots$ part shifts it so that it ranges from $0$ to $2$. This ensures that the entire term $\frac{1}{2}(\eta_{max} - \eta_{min})\left(1 + \cos\left(\frac{T_{cur}}{T_i}\pi\right)\right)$ ranges from $(\eta_{max} - \eta_{min})$ down to $0$. Adding $\eta_{min}$ then correctly shifts the range to $[\eta_{min}, \eta_{max}]$.

This mathematical formulation ensures a smooth, non-linear decay of the learning rate within each cycle, starting from $\eta_{max}$ and ending at $\eta_{min}$, before being reset for the next cycle.

## Advantages
*   **Improved Convergence:** Often leads to faster convergence and better final model performance compared to static or simple decaying learning rates.
*   **Escaping Local Minima:** The periodic warm restarts provide the optimizer with enough "energy" to jump out of sharp, suboptimal local minima, allowing it to explore the loss landscape more effectively.
*   **Finding Flatter Minima:** By encouraging exploration, it increases the chances of converging to flatter minima, which are generally associated with better generalization performance on unseen data.
*   **Robustness:** Can be more robust to the initial choice of learning rate compared to fixed schedules, as it explores a range of learning rates.
*   **Implicit Ensemble Effect:** Some research suggests that the cyclical learning rates can implicitly create an ensemble of models, as the model visits different regions of the loss landscape, leading to better overall performance.

## Disadvantages
*   **Hyperparameter Tuning:** Introduces additional hyperparameters to tune, such as $\eta_{min}$, $\eta_{max}$, initial cycle length ($T_0$), and the cycle length multiplier (e.g., factor of 2). This can increase the complexity of hyperparameter search.
*   **Increased Training Time (Potentially):** If cycle lengths are too short or the number of restarts is too high, the model might not have enough time to converge within a cycle before being reset, potentially leading to slower overall convergence or instability.
*   **Complexity:** More complex to implement and manage compared to simpler learning rate schedules like step decay or exponential decay.
*   **Sensitivity to $\eta_{max}$:** While robust, the choice of $\eta_{max}$ is still critical. If it's too high, the model might diverge at the start of each cycle.
*   **Not Always Optimal:** While generally effective, it's not a silver bullet and might not always outperform other well-tuned learning rate schedules for every specific task or dataset.

## Real World Applications
Cosine Annealing, particularly with warm restarts, has found widespread adoption across various domains in deep learning due to its effectiveness in improving model training and performance.

1.  **Computer Vision:**
    *   **Image Classification:** Used extensively in training state-of-the-art image classification models (e.g., ResNet, EfficientNet) on datasets like ImageNet. It helps achieve higher accuracy by allowing models to converge to better minima.
    *   **Object Detection and Segmentation:** Applied in training models for tasks like YOLO, Mask R-CNN, and U-Net, where precise localization and pixel-level predictions benefit from robust optimization.
    *   **Generative Adversarial Networks (GANs):** Can be used to stabilize GAN training, which is notoriously difficult, by providing a dynamic learning rate for both generator and discriminator.

2.  **Natural Language Processing (NLP):**
    *   **Transformer Models:** Widely used in training large Transformer-based models (e.g., BERT, GPT, T5) for tasks like machine translation, text summarization, and language understanding. The long training times and complex loss landscapes of these models benefit significantly from cyclical learning rates.
    *   **Recurrent Neural Networks (RNNs) and LSTMs:** Applied in older sequence models for tasks like sentiment analysis, named entity recognition, and speech recognition to improve convergence and performance.

3.  **Reinforcement Learning:**
    *   **Policy Optimization:** In complex reinforcement learning environments, training agents often involves optimizing policies over many steps. Cosine Annealing can be used to schedule the learning rate for policy networks, helping agents explore different strategies and converge to optimal policies more effectively.

4.  **Recommendation Systems:**
    *   **Deep Learning Recommenders:** When deep neural networks are used for collaborative filtering or content-based recommendations, Cosine Annealing can help train these models more efficiently, leading to better prediction accuracy for user preferences.

5.  **Medical Imaging:**
    *   **Disease Diagnosis and Prognosis:** Applied in training deep learning models for analyzing medical images (e.g., X-rays, MRIs, CT scans) for tasks like tumor detection, disease classification, and segmentation of anatomical structures, where high accuracy is critical.

## Python Example

This example demonstrates Cosine Annealing with warm restarts using PyTorch. We'll simulate a training loop and plot the learning rate schedule over epochs.

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts
import matplotlib.pyplot as plt
import numpy as np

# 1. Define a dummy model and optimizer
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.linear = nn.Linear(10, 1) # Dummy layer

    def forward(self, x):
        return self.linear(x)

model = SimpleModel()
optimizer = optim.SGD(model.parameters(), lr=0.1) # Initial learning rate for the scheduler

# 2. Configure Cosine Annealing Warm Restarts scheduler
# T_0: Number of epochs for the first restart cycle.
# T_mult: Factor by which the cycle length is multiplied after each restart.
# eta_min: Minimum learning rate.
scheduler = CosineAnnealingWarmRestarts(optimizer, T_0=5, T_mult=2, eta_min=0.001)

# 3. Simulate training over several epochs and record learning rates
num_epochs = 50
learning_rates = []

print(f"Initial LR: {optimizer.param_groups[0]['lr']:.4f}")

for epoch in range(num_epochs):
    # In a real scenario, you would perform:
    # 1. Forward pass
    # 2. Calculate loss
    # 3. Backward pass (optimizer.zero_grad(), loss.backward())
    # 4. Optimizer step (optimizer.step())

    # Record the current learning rate
    current_lr = optimizer.param_groups[0]['lr']
    learning_rates.append(current_lr)

    # Print LR for some epochs to see the change
    if (epoch + 1) % 5 == 0 or epoch == 0 or epoch == num_epochs - 1:
        print(f"Epoch {epoch + 1:2d}/{num_epochs}: LR = {current_lr:.6f}")

    # Step the scheduler. This updates the learning rate for the next epoch.
    scheduler.step()

print(f"Final LR: {optimizer.param_groups[0]['lr']:.4f}")

# 4. Plot the learning rate schedule
plt.figure(figsize=(12, 6))
plt.plot(range(num_epochs), learning_rates, marker='o', markersize=4, linestyle='-')
plt.title('Learning Rate Schedule with Cosine Annealing Warm Restarts')
plt.xlabel('Epoch')
plt.ylabel('Learning Rate')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.xticks(np.arange(0, num_epochs + 1, 5))
plt.yticks(np.arange(min(learning_rates), max(learning_rates) + 0.01, 0.01))
plt.tight_layout()
plt.show()

# Explanation of the plot:
# - The learning rate starts at 0.1 (eta_max, implicitly set by optimizer's lr).
# - It decays following a cosine curve for 5 epochs (T_0=5).
# - At epoch 5, it "restarts" back to 0.1.
# - The next cycle length is T_0 * T_mult = 5 * 2 = 10 epochs.
# - It decays for 10 epochs, then restarts at epoch 15.
# - The next cycle length is 10 * 2 = 20 epochs.
# - It decays for 20 epochs, then restarts at epoch 35.
# - The next cycle length would be 20 * 2 = 40 epochs, but our num_epochs is 50,
#   so the last cycle is cut short.
# - The learning rate never drops below eta_min=0.001.
```

**Explanation of the Code:**

1.  **Dummy Model and Optimizer:** We create a very simple `nn.Module` and an `optim.SGD` optimizer. The `lr` passed to `optim.SGD` here acts as the initial `eta_max` for the scheduler.
2.  **`CosineAnnealingWarmRestarts`:**
    *   `optimizer`: The optimizer whose learning rate will be scheduled.
    *   `T_0=5`: The first cycle will last for 5 epochs.
    *   `T_mult=2`: After each restart, the length of the next cycle will be multiplied by 2. So, cycles will be 5, 10, 20, 40... epochs long.
    *   `eta_min=0.001`: The learning rate will not go below 0.001 within any cycle.
3.  **Simulation Loop:** We iterate for `num_epochs`. In each epoch:
    *   We record the current learning rate from the optimizer's parameter groups.
    *   `scheduler.step()`: This is the crucial line. It updates the learning rate for the *next* epoch based on the Cosine Annealing Warm Restarts schedule.
4.  **Plotting:** The collected learning rates are plotted against the epoch number to visually demonstrate the cyclical decay and warm restarts. You can clearly see the learning rate dropping and then jumping back up, with the decay periods getting longer.

## Interview Questions

1.  **What is Cosine Annealing and why is it used in deep learning?**
    *   **Answer:** Cosine Annealing is a learning rate scheduling strategy that adjusts the learning rate during training. It typically involves decaying the learning rate following a cosine curve within a cycle, and often includes "warm restarts" where the learning rate is reset to a higher value periodically. It's used to help models escape suboptimal local minima, explore the loss landscape more effectively, and converge to flatter, better-generalizing minima, leading to improved training stability and final model performance.

2.  **Explain the concept of "warm restarts" in the context of Cosine Annealing.**
    *   **Answer:** Warm restarts refer to the mechanism where, after the learning rate has decayed to its minimum value at the end of a cycle, it is suddenly reset back to its maximum value. This provides a "jolt" to the optimizer, giving it renewed momentum to jump out of any local minimum it might have settled into. It encourages exploration of different regions of the loss landscape, preventing the model from getting stuck.

3.  **How does Cosine Annealing differ from a simple step decay or exponential decay learning rate schedule?**
    *   **Answer:**
        *   **Step Decay/Exponential Decay:** These schedules monotonically decrease the learning rate over time. Once the learning rate drops, it generally stays low or continues to decrease. They don't have a mechanism to increase the learning rate again.
        *   **Cosine Annealing (especially with warm restarts):** It's cyclical. The learning rate decreases within a cycle but then periodically resets to a higher value. This allows for both fine-tuning (during decay) and exploration (during restarts), which is a key differentiator.

4.  **What are the key hyperparameters you need to tune for Cosine Annealing with warm restarts?**
    *   **Answer:**
        *   `eta_max` (or initial learning rate): The maximum learning rate at the start of each cycle.
        *   `eta_min`: The minimum learning rate at the end of each cycle.
        *   `T_0`: The number of epochs (or batches) in the first cycle.
        *   `T_mult`: The factor by which the cycle length is multiplied after each restart (e.g., 1 for fixed cycle length, 2 for doubling).

5.  **What is the mathematical formula for Cosine Annealing and what does each term represent?**
    *   **Answer:** The formula is $\eta_t = \eta_{min} + \frac{1}{2}(\eta_{max} - \eta_{min})\left(1 + \cos\left(\frac{T_{cur}}{T_i}\pi\right)\right)$.
        *   $\eta_t$: Learning rate at time $t$.
        *   $\eta_{min}$: Minimum learning rate in a cycle.
        *   $\eta_{max}$: Maximum learning rate in a cycle.
        *   $T_{cur}$: Number of epochs/batches since the last restart.
        *   $T_i$: Total number of epochs/batches in the current cycle.
        *   $\pi$: Mathematical constant pi.

6.  **Why is a cosine function used for the decay, rather than a linear decay?**
    *   **Answer:** A cosine function provides a smoother, non-linear decay. It decays slowly at the beginning and end of the cycle and faster in the middle. This allows for larger steps initially when the model is far from a minimum, and then very fine-grained adjustments as it approaches the minimum, without the abruptness of a linear decay. The smooth transition is generally more beneficial for optimization.

7.  **What are the potential benefits of using Cosine Annealing over a fixed learning rate?**
    *   **Answer:**
        *   Better convergence to optimal solutions.
        *   Ability to escape local minima.
        *   Improved generalization performance by finding flatter minima.
        *   More robust training dynamics.
        *   Potentially faster training by allowing higher learning rates initially.

8.  **Are there any drawbacks or situations where Cosine Annealing might not be ideal?**
    *   **Answer:** Yes. It introduces more hyperparameters to tune, which can increase the complexity of hyperparameter search. If the cycle lengths are too short, the model might not fully converge within a cycle, leading to instability. It's also more complex to implement than simpler schedules. In some very specific tasks or architectures, a simpler, well-tuned schedule might perform comparably or even better.

9.  **How does increasing the cycle length (`T_mult > 1`) affect the training process?**
    *   **Answer:** Increasing the cycle length after each restart means that subsequent cycles are longer. This allows the model to spend progressively more time exploring and fine-tuning within a given region of the loss landscape before the next restart. It can be beneficial as training progresses, allowing for more thorough convergence in later stages while still retaining the exploration benefits of restarts.

10. **In which real-world applications has Cosine Annealing proven particularly effective?**
    *   **Answer:** Cosine Annealing has been highly effective in:
        *   **Computer Vision:** Training state-of-the-art models for image classification, object detection, and segmentation (e.g., with ResNets, Transformers).
        *   **Natural Language Processing:** Optimizing large Transformer models like BERT and GPT for various NLP tasks.
        *   **Reinforcement Learning:** Scheduling learning rates for policy networks in complex RL environments.
        *   Generally, any deep learning task with complex loss landscapes and long training times benefits from its exploration capabilities.

## Quiz

1.  **What is the primary goal of Cosine Annealing with warm restarts?**
    A) To keep the learning rate constant throughout training.
    B) To monotonically decrease the learning rate to zero.
    C) To help the model escape local minima and find better global minima.
    D) To increase the batch size dynamically during training.

2.  **Which of the following best describes the learning rate behavior within a single cycle of Cosine Annealing?**
    A) It linearly increases from minimum to maximum.
    B) It linearly decreases from maximum to minimum.
    C) It decays from a maximum to a minimum following a cosine curve.
    D) It remains constant for the entire cycle.

3.  **What does the hyperparameter `T_0` represent in `CosineAnnealingWarmRestarts`?**
    A) The total number of training epochs.
    B) The minimum learning rate.
    C) The number of epochs for the first restart cycle.
    D) The factor by which the learning rate is multiplied.

4.  **A key advantage of Cosine Annealing is its ability to find "flatter minima." Why are flatter minima generally preferred in deep learning?**
    A) They are easier to reach during optimization.
    B) They correspond to models that generalize better to unseen data.
    C) They require less computational resources to train.
    D) They always have a lower training loss.

5.  **If `T_mult` is set to 1 in `CosineAnnealingWarmRestarts`, what does this imply about the cycle lengths?**
    A) The cycle length will continuously increase.
    B) The cycle length will continuously decrease.
    C) The cycle length will remain constant for all cycles.
    D) The scheduler will only run for one cycle.

---

### Answer Key

1.  **C) To help the model escape local minima and find better global minima.**
    *   **Explanation:** The cyclical nature and warm restarts of Cosine Annealing are specifically designed to prevent the model from getting stuck in suboptimal local minima and encourage exploration of the loss landscape to find better, potentially global, minima.

2.  **C) It decays from a maximum to a minimum following a cosine curve.**
    *   **Explanation:** The name "Cosine Annealing" directly refers to the use of a cosine function to smoothly decay the learning rate from its maximum to its minimum value within each cycle.

3.  **C) The number of epochs for the first restart cycle.**
    *   **Explanation:** `T_0` explicitly defines the duration of the very first cycle before the first warm restart occurs. Subsequent cycle lengths are then derived from `T_0` and `T_mult`.

4.  **B) They correspond to models that generalize better to unseen data.**
    *   **Explanation:** Flatter minima are generally considered more robust to small perturbations in the input data or model parameters, which translates to better generalization performance on new, unseen data. Sharp minima are more sensitive to these changes.

5.  **C) The cycle length will remain constant for all cycles.**
    *   **Explanation:** If `T_mult` is 1, then `T_i = T_{i-1} * 1`, meaning the cycle length will not change after the initial `T_0`. Each cycle will have the same duration.

## Further Reading

1.  **SGDR: Stochastic Gradient Descent with Warm Restarts (Original Paper):**
    *   **Link:** [https://arxiv.org/abs/1608.03983](https://arxiv.org/abs/1608.03983)
    *   **Description:** The foundational paper by Ilya Loshchilov and Frank Hutter that introduced the concept of warm restarts and cosine annealing for learning rate scheduling. Essential for a deep dive into the mathematical and empirical motivations.

2.  **PyTorch Documentation for `CosineAnnealingWarmRestarts`:**
    *   **Link:** [https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CosineAnnealingWarmRestarts.html](https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.CosineAnnealingWarmRestarts.html)
    *   **Description:** Official documentation providing details on how to use the scheduler in PyTorch, including parameters and usage examples. A practical resource for implementation.

3.  **"The Little Book of Deep Learning" by Frank Hutter (Chapter on Learning Rate Schedules):**
    *   **Link:** [https://www.automl.org/wp-content/uploads/2020/07/little_book_of_deep_learning.pdf](https://www.automl.org/wp-content/uploads/2020/07/little_book_of_deep_learning.pdf) (See Chapter 5, "Optimization")
    *   **Description:** A comprehensive and accessible textbook that covers various aspects of deep learning, including a dedicated section on learning rate schedules, where Cosine Annealing is discussed in detail alongside other techniques.