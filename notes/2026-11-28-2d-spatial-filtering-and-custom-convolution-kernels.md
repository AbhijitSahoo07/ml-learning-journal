# 2D Spatial Filtering and Custom Convolution Kernels

### Core Concept
2D spatial filtering transforms an image by sliding a small matrix (kernel) over pixels to extract features or alter appearances. It forms the foundational operation of Convolutional Neural Networks (CNNs) for computer vision tasks.

### Key Mechanism & Intuition
A kernel computes the element-wise product with an overlapping image patch, summing the results into a single output pixel: $S(i,j) = \sum_m \sum_n I(i+m, j+n)K(m,n)$. Custom kernels manually define transformations—like Sobel for edge detection or Gaussian for smoothing—whereas CNNs learn these kernel weights automatically via backpropagation.

### Key Takeaway
- Handcrafted kernels provide fixed mathematical operations; modern deep learning replaces manual design by learning optimal task-specific filters directly from data.