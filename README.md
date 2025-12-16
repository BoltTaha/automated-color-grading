# Automated Color Grading Tool (Reinhard Method)

Steal the 'Golden Hour' look from any photo. 🌅 A Python tool that automatically clones color aesthetics using statistical analysis (No AI required).

## Description

A Python-based Computer Vision tool that automates color grading by statistically transferring the aesthetic style of a reference image to a target image. It utilizes the LAB Color Space to separate luminance from chrominance, ensuring accurate exposure normalization while preserving the original content's structure.

## 📸 Results Showcase

Here is a demo of the tool in action. The script extracts the 'Golden Hour' color palette from the reference (left) and statistically transfers it to a dull, overcast photo (center), creating a warm, sunlit result (right) automatically.

### Reference Image (Style Source)
<img src="reference_sunset.jpg" alt="Reference Sunset Image" width="800"/>

### Before & After Comparison

| Before | After |
|--------|-------|
| <img src="target_forest.jpg" alt="Original Target Image" width="400"/> | <img src="output/processed_target_forest.jpg" alt="Processed Image with Color Transfer" width="400"/> |

**Original Target Image** → **Processed with Reference Style Applied**

## Key Features

- **Algorithm**: Implements the Reinhard Statistical Color Transfer method.
- **Luminance Clamp**: Custom adaptive thresholding to prevent blown-out highlights in bright images.
- **Saturation Preservation**: Modified logic to apply tint without destroying the variance (vibrancy) of neon/saturated objects.
- **Zero-AI Dependency**: Deterministic output using pure numpy and OpenCV mathematics.

## Requirements

- Python 3.7 or higher
- Dependencies: numpy, opencv-python, Pillow

## Installation

```bash
pip install -r requirements.txt
```

## How to Run

```bash
python color_transfer.py reference.jpg target.jpg
```

The processed image will be saved in the `output/` directory.

---

## Technical Details

- **Deterministic**: Same inputs → same outputs
- **No AI/ML**: Pure statistical color transfer
- **Adaptive**: Prevents over-exposure in bright images
- **Preserves Structure**: Only transfers color statistics, maintains image details
- **OpenCV LAB Range**: Correctly handles 0-255 range for all channels (L, A, B)

### How It Works

1. **Style Extraction**: Convert reference image to LAB color space and extract statistical characteristics (mean and standard deviation) for L (luminance), A (green-red), and B (blue-yellow) channels.

2. **Exposure Normalization**: Normalize exposure using adaptive luminance adjustment to prevent blown-out highlights in bright images.

3. **Color Transfer**: Apply statistical color transfer to A and B channels by matching mean and standard deviation from reference, preserving image structure while transferring color characteristics.

4. **Output**: Processed images are saved in the `output/` directory.

### Why LAB Color Space?

LAB separates luminance (L) from chrominance (A, B), allowing independent control of exposure and color, which is essential for handling mixed lighting conditions while maintaining aesthetic quality.

## File Structure

- `color_transfer.py` - Main script with core color transfer functions
- `requirements.txt` - Python package dependencies
- `README.md` - Documentation
- `output/` - Directory containing processed images

## Topics

`python` `opencv` `computer-vision` `image-processing` `color-science` `automation`

---

## Author

**Muhammad Taha**

<div align="center">

⭐ Star this repo if you found it helpful!

**Made with ❤️ for professional color grading**

</div>
