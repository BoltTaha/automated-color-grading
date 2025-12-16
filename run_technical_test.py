"""
Luminafix Technical Test - Run with Client's Images
====================================================
This script processes the specific images provided for the technical test.
"""

from color_transfer import process_images

# Client-provided images
REFERENCE_IMAGE = 'reference_sunset.jpg'
TARGET_IMAGES = [
    'target_forest.jpg'
]
OUTPUT_DIR = 'output'

if __name__ == '__main__':
    print("=" * 70)
    print("LUMINAFIX TECHNICAL TEST - PROCESSING CLIENT IMAGES")
    print("=" * 70)
    print(f"\nReference: {REFERENCE_IMAGE}")
    print(f"Targets: {len(TARGET_IMAGES)} images")
    print(f"Output: {OUTPUT_DIR}/")
    print("\n" + "-" * 70 + "\n")
    
    try:
        process_images(REFERENCE_IMAGE, TARGET_IMAGES, OUTPUT_DIR)
        print("\n" + "=" * 70)
        print("[SUCCESS] TECHNICAL TEST COMPLETE!")
        print("=" * 70)
        print(f"\nProcessed images saved in: {OUTPUT_DIR}/")
        print("\nFiles created:")
        print("  - processed_target_forest.jpg")
        print("\nReady for submission to client!")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

