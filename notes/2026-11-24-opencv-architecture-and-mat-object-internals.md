# OpenCV Architecture and Mat Object Internals

### Core Concept
OpenCV is a modular, high-performance computer vision library, centered on the `cv::Mat` n-dimensional dense array. It provides the computational foundation for image preprocessing in modern computer vision and deep learning pipelines.

### Key Mechanism & Intuition
A `cv::Mat` consists of a lightweight header (storing metadata like dimensions, type, and step) and a pointer to the pixel data. Copying a `Mat` performs a shallow copy by default, duplicating only the header and incrementing an internal reference counter. To locate pixel $(r, c)$, it calculates the memory offset via $\text{offset} = r \times \text{step} + c \times \text{elemSize}$.

### Key Takeaway
* `Mat A = B` creates a shared memory reference; use `B.clone()` to avoid accidental side effects.