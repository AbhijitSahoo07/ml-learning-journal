# Bitwise Logical Operations on Images (AND, OR, XOR, NOT)

### Core Concept
Bitwise operations apply Boolean logic at the individual pixel level, enabling precise image masking and region-of-interest extraction. They are foundational preprocessing steps in computer vision for segmenting relevant features and removing noise before model training.

### Key Mechanism & Intuition
Pixels are represented as binary values (0 to 255). Operations execute per-bit:
* **AND:** Retains pixels where both images/masks are active (extracts target regions).
* **OR:** Combines non-zero pixels from both inputs.
* **XOR:** Highlights differences ($1 \oplus 1 = 0$, $1 \oplus 0 = 1$).
* **NOT:** Inverts pixel values ($255 - P$).

### Key Takeaway
* **Essential for masking:** Use bitwise **AND** with binary masks to isolate complex object shapes efficiently.