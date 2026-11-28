# Image Smoothing: Gaussian Blurring and Kernel Standard Deviation

### Core Concept
Gaussian blurring is an image pre-processing technique that reduces high-frequency noise and detail by convolving an image with a Gaussian function. It prevents computer vision models from overfitting to irrelevant pixel-level noise.

### Key Mechanism & Intuition
The filter computes a weighted average of neighboring pixels using a 2D Gaussian distribution: $G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$. The standard deviation ($\sigma$) controls the spread; larger $\sigma$ values assign higher weights to distant pixels, producing a stronger, wider blur.

### Key Takeaway
* Larger $\sigma$ smooths more noise but destroys edge sharpness; kernel size is typically set to $\approx 6\sigma + 1$ to capture $99\%$ of the distribution.