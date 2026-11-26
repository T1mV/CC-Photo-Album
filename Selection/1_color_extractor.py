import os
import numpy as np
from PIL import Image
from pillow_heif import register_heif_opener

# Enable Pillow to read iPhone HEIC/HEIF images
register_heif_opener()

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif")

def extract_hsv_vector(img_rgb, bins=(8, 4, 4)): #8group RGB, 4 hue, 4 saturation
    #Convert the RGB image into 128 dim HSV
    small = img_rgb.resize((150, 150))
    img_hsv = small.convert("HSV")
    arr = np.array(img_hsv)

    hist, _ = np.histogramdd(
        arr.reshape(-1, 3),
        bins=bins,
        range=[(0, 256), (0, 256), (0, 256)]
    )
    # Normalize vector length to 1 for consistent distance calculation
    norm = np.linalg.norm(hist)
    if norm > 0:
        hist = hist / norm
    return hist.flatten()


def get_orientation(width, height):
    # get the orientation of the image
    ratio = width / height
    if ratio > 1.05:
        return "landscape"
    elif ratio < 0.95:
        return "portrait"
    return "square"


def process_folder(image_dir="images"):
    # Read the images
    results = []

    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"Directory '{image_dir}' not found.")

    for filename in sorted(os.listdir(image_dir)):
        if not filename.lower().endswith(SUPPORTED_EXTENSIONS):
            continue

        filepath = os.path.join(image_dir, filename)
        try:
            with Image.open(filepath) as img:
                width, height = img.size
                # Skip low resolution thumbnails
                if max(width, height) < 500:
                    continue

                img_rgb = img.convert("RGB")
                vector = extract_hsv_vector(img_rgb)
                orientation = get_orientation(width, height)

                results.append({
                    "filename": filename,
                    "filepath": filepath,
                    "width": width,
                    "height": height,
                    "orientation": orientation,
                    "hero_eligible": max(width, height) >= 1200, #to be applicable as cover picture
                    "vector": vector
                })
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    return results


if __name__ == "__main__":
    data = process_folder("images")
    print(f"Successfully processed {len(data)} images.\n")
