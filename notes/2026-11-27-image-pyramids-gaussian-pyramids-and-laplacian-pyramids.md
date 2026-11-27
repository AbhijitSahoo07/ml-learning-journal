# Image Pyramids: Gaussian Pyramids and Laplacian Pyramids

### Core Concept
Image pyramids are multi-scale representations used to process visual features across varying resolutions. They are fundamental in computer vision for scale-invariant object detection, image blending, and compression.

### Key Mechanism & Intuition
A **Gaussian Pyramid** recursively blurs an image with a low-pass filter and downsamples it (subsampling by 2). A **Laplacian Pyramid** captures high-frequency details (edges) lost at each level. It is computed by subtracting the upsampled, blurred image from the original: $L_i = G_i - \text{expand}(G_{i+1})$.

### Key Takeaway
- **Gaussian**: Captures coarse structure (downsampling/smoothing).
- **Laplacian**: Captures edge residuals, enabling perfect image reconstruction and multi-band blending.