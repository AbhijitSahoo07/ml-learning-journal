# Image Arithmetic and Alpha Blending in OpenCV

### Core Concept
Image arithmetic performs pixel-wise operations to modify brightness, contrast, or combine inputs. Alpha blending enables seamless image composition and data augmentation (like Mixup) for robust machine learning models.

### Key Mechanism & Intuition
Unlike NumPy's modulo addition, OpenCV’s `cv2.add()` uses saturated arithmetic, clipping values at 255 to prevent overflow artifacts. Alpha blending calculates a weighted sum of two images using the formula:  
$$g(x) = (1 - \alpha)f_0(x) + \alpha f_1(x) + \gamma$$  
Implemented via `cv2.addWeighted()`, it smoothly transitions transparency between images of identical dimensions.

### Key Takeaway
- Always use `cv2.add()` over `+` to avoid 8-bit integer rollover.
- Crucial preprocessing technique for watermark overlays and synthetic training data generation.