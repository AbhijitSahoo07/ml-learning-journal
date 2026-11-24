# OpenCV Coordinate System and Pixel Indexing

### Core Concept
In computer vision, OpenCV models images as 2D grids originating from the top-left corner $(0,0)$. Understanding its coordinate conventions is critical for correct spatial data manipulation, data augmentation, and bounding-box modeling.

### Key Mechanism & Intuition
OpenCV geometric functions (like drawing shapes) use Cartesian coordinates $(x, y)$, where $x$ represents horizontal width and $y$ represents vertical height. Conversely, pixel-level array indexing uses standard NumPy matrix row-column order: `image[y, x]`. For a 2D image coordinate $(x, y)$, the pixel intensity is accessed as $I(y, x)$ or `image[row, col]`.

### Key Takeaway
- OpenCV drawing functions use $(x, y) = (\text{width}, \text{height})$.
- NumPy pixel slicing uses $(y, x) = (\text{row}, \text{column})$. Mixing these up causes common transposition bugs.