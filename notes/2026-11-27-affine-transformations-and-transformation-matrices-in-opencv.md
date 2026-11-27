# Affine Transformations and Transformation Matrices in OpenCV

### Core Concept
An affine transformation is a geometric mapping that preserves points, straight lines, and parallelism. In machine learning, it is crucial for data augmentation, image registration, and standardizing inputs across computer vision pipelines.

### Key Mechanism & Intuition
It maps original coordinates $(x, y)$ to $(x', y')$ using a $2 \times 3$ transformation matrix $M$:

$$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} + \begin{bmatrix} t_x \\ t_y \end{bmatrix}$$

This combines linear transformations (scaling, rotation, shear) with translation. In OpenCV, `cv2.getAffineTransform()` computes $M$ from three non-collinear point pairs, and `cv2.warpAffine()` applies it.

### Key Takeaway
* Preserves line parallelism, but not necessarily lengths or angles.
* Requires exactly three point correspondences to define the full transformation matrix.