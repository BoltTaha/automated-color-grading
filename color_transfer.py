"""
Luminafix Technical Test - Color Transfer Script
=================================================
Extracts tone/color characteristics from a reference image and applies them
to target images using LAB color space statistical transfer with exposure normalization.

Author: Muhammad Taha
Date: Technical Test Submission
"""

import numpy as np
from PIL import Image
import cv2
import os
import argparse
from pathlib import Path


def extract_reference_characteristics(reference_path):
    """
    Extract basic tone and color characteristics from reference image.
    
    Returns:
        dict: Statistics including mean, std for LAB channels
    """
    # Load reference image
    ref_img = cv2.imread(reference_path)
    if ref_img is None:
        raise ValueError(f"Could not load reference image: {reference_path}")
    
    # Convert BGR to RGB (OpenCV uses BGR)
    ref_rgb = cv2.cvtColor(ref_img, cv2.COLOR_BGR2RGB)
    
    # Convert RGB to LAB color space
    ref_lab = cv2.cvtColor(ref_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    
    # Calculate statistics for each channel
    # L: Luminance (lightness), A: Green-Red, B: Blue-Yellow
    l_mean, l_std = ref_lab[:, :, 0].mean(), ref_lab[:, :, 0].std()
    a_mean, a_std = ref_lab[:, :, 1].mean(), ref_lab[:, :, 1].std()
    b_mean, b_std = ref_lab[:, :, 2].mean(), ref_lab[:, :, 2].std()
    
    characteristics = {
        'l_mean': l_mean,
        'l_std': l_std,
        'a_mean': a_mean,
        'a_std': a_std,
        'b_mean': b_mean,
        'b_std': b_std
    }
    
    return characteristics


def normalize_exposure_luminance(img_lab, target_l_mean, target_l_std, adaptive=True):
    """
    Normalize exposure by adjusting luminance channel.
    Uses adaptive logic to prevent blown-out highlights.
    
    Args:
        img_lab: Image in LAB color space
        target_l_mean: Target luminance mean from reference
        target_l_std: Target luminance std from reference
        adaptive: If True, uses adaptive formula to prevent over-exposure
    
    Returns:
        Normalized LAB image
    """
    img_lab_norm = img_lab.copy()
    current_l = img_lab[:, :, 0]
    
    # Current statistics
    current_l_mean = current_l.mean()
    current_l_std = current_l.std()
    
    if adaptive:
        # Adaptive luminance adjustment formula
        # Prevents blown-out highlights by reducing adjustment for bright areas
        # Formula: Adjustment = (Target_L - Current_L) * (1 - Current_L_normalized)
        
        # Normalize current luminance to 0-1 range for safety calculation
        # CRITICAL FIX: OpenCV LAB L channel is 0-255 (8-bit), not 0-100
        current_l_normalized = current_l / 255.0
        
        # Calculate desired adjustment
        target_adjustment = target_l_mean - current_l_mean
        
        # Apply adaptive scaling: reduce adjustment for bright areas
        # Bright areas (high L) get less adjustment to prevent blowout
        safety_factor = 1.0 - (current_l_normalized * 0.5)  # Reduce adjustment by up to 50% for bright areas
        safety_factor = np.clip(safety_factor, 0.3, 1.0)  # Keep at least 30% adjustment
        
        # Apply mean shift with adaptive scaling
        adjusted_l = current_l + (target_adjustment * safety_factor)
        
        # Normalize standard deviation (contrast adjustment)
        if current_l_std > 0:
            adjusted_l = (adjusted_l - adjusted_l.mean()) * (target_l_std / current_l_std) + adjusted_l.mean()
    else:
        # Standard normalization (mean and std matching)
        adjusted_l = (current_l - current_l_mean) * (target_l_std / current_l_std) + target_l_mean
    
    # Clip to valid OpenCV LAB range (0-255 for L channel)
    adjusted_l = np.clip(adjusted_l, 0, 255)
    
    img_lab_norm[:, :, 0] = adjusted_l
    
    return img_lab_norm


def apply_color_transfer(target_path, reference_chars, output_path):
    """
    Apply color transfer (Reinhard method) with Saturation Preservation.
    """
    target_img = cv2.imread(target_path)
    if target_img is None:
        raise ValueError(f"Could not load target image: {target_path}")
    
    # Convert BGR to RGB
    target_rgb = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)
    
    # Convert RGB to LAB (OpenCV range 0-255)
    target_lab = cv2.cvtColor(target_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    
    # Step 1: Normalize Exposure (L Channel)
    target_lab_normalized = normalize_exposure_luminance(
        target_lab,
        reference_chars['l_mean'],
        reference_chars['l_std'],
        adaptive=True
    )
    
    # Step 2: Color Transfer (A & B Channels)
    current_a = target_lab_normalized[:, :, 1]
    current_b = target_lab_normalized[:, :, 2]
    
    current_a_mean, current_a_std = current_a.mean(), current_a.std()
    current_b_mean, current_b_std = current_b.mean(), current_b.std()
    
    # --- SATURATION PRESERVATION LOGIC ---
    # Calculate strict Reinhard scaling
    a_scale_strict = reference_chars['a_std'] / (current_a_std + 1e-5)
    b_scale_strict = reference_chars['b_std'] / (current_b_std + 1e-5)
    
    # Blend with 1.0 to preserve original saturation (0.8 = 80% original saturation)
    saturation_preservation = 0.8
    a_scale = (a_scale_strict * (1.0 - saturation_preservation)) + (1.0 * saturation_preservation)
    b_scale = (b_scale_strict * (1.0 - saturation_preservation)) + (1.0 * saturation_preservation)

    # Apply Transfer
    if current_a_std > 0:
        target_lab_normalized[:, :, 1] = (current_a - current_a_mean) * a_scale + reference_chars['a_mean']
    
    if current_b_std > 0:
        target_lab_normalized[:, :, 2] = (current_b - current_b_mean) * b_scale + reference_chars['b_mean']
    
    # Clip to valid range (0-255)
    target_lab_normalized[:, :, 1] = np.clip(target_lab_normalized[:, :, 1], 0, 255)
    target_lab_normalized[:, :, 2] = np.clip(target_lab_normalized[:, :, 2], 0, 255)
    
    # Convert back to RGB -> BGR
    target_lab_uint8 = target_lab_normalized.astype(np.uint8)
    result_rgb = cv2.cvtColor(target_lab_uint8, cv2.COLOR_LAB2RGB)
    result_bgr = cv2.cvtColor(result_rgb, cv2.COLOR_RGB2BGR)
    
    cv2.imwrite(output_path, result_bgr)
    print(f"[OK] Processed: {Path(target_path).name} -> {Path(output_path).name}")


def process_images(reference_path, target_paths, output_dir='output'):
    """
    Main processing function.
    
    Args:
        reference_path: Path to reference image
        target_paths: List of paths to target images
        output_dir: Directory to save processed images
    """
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print("Luminafix Color Transfer - Technical Test")
    print("=" * 60)
    print(f"\nReference image: {Path(reference_path).name}")
    print(f"Target images: {len(target_paths)}")
    print(f"Output directory: {output_dir}\n")
    
    # Step 1: Extract reference characteristics
    print("Step 1: Extracting reference characteristics...")
    reference_chars = extract_reference_characteristics(reference_path)
    print(f"  Reference L: mean={reference_chars['l_mean']:.2f}, std={reference_chars['l_std']:.2f}")
    print(f"  Reference A: mean={reference_chars['a_mean']:.2f}, std={reference_chars['a_std']:.2f}")
    print(f"  Reference B: mean={reference_chars['b_mean']:.2f}, std={reference_chars['b_std']:.2f}\n")
    
    # Step 2: Process each target image
    print("Step 2: Processing target images...")
    for i, target_path in enumerate(target_paths, 1):
        output_filename = f"processed_{Path(target_path).stem}.jpg"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            apply_color_transfer(target_path, reference_chars, output_path)
        except Exception as e:
            print(f"[ERROR] Error processing {Path(target_path).name}: {e}")
    
    print("\n" + "=" * 60)
    print("Processing complete!")
    print(f"Results saved in: {output_dir}")
    print("=" * 60)


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Apply color transfer from reference to target images using LAB color space.'
    )
    parser.add_argument(
        'reference',
        type=str,
        help='Path to reference image'
    )
    parser.add_argument(
        'targets',
        type=str,
        nargs='+',
        help='Paths to target images (3 images expected)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='output',
        help='Output directory (default: output)'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if not os.path.exists(args.reference):
        print(f"Error: Reference image not found: {args.reference}")
        return
    
    for target in args.targets:
        if not os.path.exists(target):
            print(f"Error: Target image not found: {target}")
            return
    
    # Process images
    process_images(args.reference, args.targets, args.output)


if __name__ == '__main__':
    main()

