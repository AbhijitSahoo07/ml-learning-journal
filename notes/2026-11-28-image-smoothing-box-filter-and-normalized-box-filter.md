# Image Smoothing: Box Filter and Normalized Box Filter

### Core Concept
A box filter is a spatial convolution filter used for image smoothing and noise reduction by averaging neighboring pixel intensities. It serves as a foundational preprocessing step in computer vision to reduce high-frequency noise before edge detection or classification.

### Key Mechanism & Intuition
An unnormalized box filter has a kernel of identical ones, which merely sums surrounding pixel values and brightens the image. The **normalized box filter** divides this kernel by its area ($K = \frac{1}{M \times N} \mathbf{1}_{M \times N}$), computing the local arithmetic mean to blur the image while preserving overall brightness and energy.

### Key Takeaway
- Fast to compute via integral images, but causes harsh square-shaped artifacts compared to Gaussian blur.