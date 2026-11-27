# Geometric Transformations: Image Resizing and Interpolation Methods

### Core Concept
Image resizing modifies spatial dimensions to standardize inputs for neural networks. Because pixel coordinates map to non-integer locations, interpolation methods estimate unknown pixel values to prevent distortion.

### Key Mechanism & Intuition
Resizing uses reverse mapping: for a target pixel $(x, y)$, it finds source coordinates and interpolates intensity. **Nearest-Neighbor** selects the closest pixel, causing pixelation. **Bilinear** uses a weighted average of the 4 surrounding pixels via $f(x,y) \approx \sum w_i I_i$. **Bicubic** fits a 16-pixel cubic spline for smoother gradients at higher computational cost.

### Key Takeaway
- Use **Bilinear** or **Bicubic** for downsampling natural images to retain features.
- Strictly use **Nearest-Neighbor** for segmentation masks to preserve discrete class labels.