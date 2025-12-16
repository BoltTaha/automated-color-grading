"""
Automated Color Grading - Test Script
======================================
This script processes images using the color transfer algorithm.
"""

from color_transfer import process_images

# Reference and target images
REFERENCE_IMAGE = 'reference_sunset.jpg'
TARGET_IMAGES = [
    'target_forest.jpg'
]
OUTPUT_DIR = 'output'

if __name__ == '__main__':
    print("=" * 70)
    print("AUTOMATED COLOR GRADING - PROCESSING IMAGES")
    print("=" * 70)
    print(f"\nReference: {REFERENCE_IMAGE}")
    print(f"Targets: {len(TARGET_IMAGES)} images")
    print(f"Output: {OUTPUT_DIR}/")
    print("\n" + "-" * 70 + "\n")
    
    try:
        process_images(REFERENCE_IMAGE, TARGET_IMAGES, OUTPUT_DIR)
        print("\n" + "=" * 70)
        print("[SUCCESS] PROCESSING COMPLETE!")
        print("=" * 70)
        print(f"\nProcessed images saved in: {OUTPUT_DIR}/")
        print("\nFiles created:")
        print("  - processed_target_forest.jpg")
        print("\nReady!")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

