# Perspective Transformation and Homography Warping in OpenCV

### Core Concept
Perspective transformation maps points from one planar view to another, correcting viewpoint distortion or aligning images. In computer vision, it is essential for image rectification, document scanning, and augmented reality alignment.

### Key Mechanism & Intuition
A $3 \times 3$ Homography matrix $H$ with 8 degrees of freedom maps 2D coordinates via $x' \sim Hx$. In OpenCV, `cv2.findHomography()` computes $H$ from at least four point correspondences (using RANSAC to reject outliers), and `cv2.warpPerspective()` applies this transformation to warp the source image into the target perspective.

### Key Takeaway
* Requires a minimum of four point pairs; always combine with RANSAC to handle noisy feature matches.