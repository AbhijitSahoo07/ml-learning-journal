# Geometric Transformations: Image Translation and Rotation

### Core Concept
Translation shifts pixel coordinates, while rotation turns an image around a pivot. They are essential data augmentation techniques in computer vision, enforcing spatial invariance in convolutional neural networks (CNNs).

### Key Mechanism & Intuition
Both operations map original coordinates $(x, y)$ to new coordinates $(x', y')$ using $2\times3$ affine transformation matrices. 
- **Translation:** Adds directional offsets: $x' = x + t_x$, $y' = y + t_y$.
- **Rotation:** Applies trigonometric mapping around angle $\theta$: 
$$\begin{bmatrix} x' \\ y' \end{bmatrix} = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix}$$
To prevent pixelated gaps, implementations apply *inverse mapping* with bilinear interpolation.

### Key Takeaway
- While CNNs are inherently translation-equivariant, they are not rotation-invariant; rotational augmentation is critical to generalize orientation-agnostic tasks.