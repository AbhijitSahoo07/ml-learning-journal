# Color Spaces and Conversions in OpenCV (BGR, RGB, HSV, HSL, LAB, YCrCb)

### Core Concept
Color spaces are mathematical models representing pixel intensities across distinct channels. In computer vision, converting between them isolates chromatic information from illumination changes to improve feature extraction and model robustness.

### Key Mechanism & Intuition
OpenCV loads images in **BGR** by default, requiring conversion via `cv2.cvtColor()`. While RGB/BGR mixes color and luminance, **HSV/HSL** decouples tone (Hue $H$) from brightness (Value/Lightness), ideal for color-based thresholding. **LAB** and **YCrCb** similarly isolate lightness ($L$ or $Y$) from chrominance, enabling illumination-invariant processing and contrast enhancement like histogram equalization.

### Key Takeaway
* Convert to **HSV** for color segmentation; use **LAB/YCrCb** to normalize lighting variations across inputs.