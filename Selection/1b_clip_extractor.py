import os
import numpy as np
from PIL import Image
from pillow_heif import register_heif_opener
from sentence_transformers import SentenceTransformer

register_heif_opener()

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif")


def get_orientation(width, height):
    ratio = width / height
    if ratio > 1.05:
        return "landscape"
    elif ratio < 0.95:
        return "portrait"
    return "square"


def process_folder(image_dir="images", model_name="clip-ViT-B-32", batch_size=16):
    # Read the images and extract normalized 512-dim CLIP semantic vectors."""
    if not os.path.exists(image_dir):
        raise FileNotFoundError(f"Directory '{image_dir}' not found.")

    metadata_list = []
    pil_images = []

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
                # Downscale in memory before batch encoding to keep CPU RAM usage low
                img_rgb.thumbnail((512, 512))

                pil_images.append(img_rgb)
                metadata_list.append({
                    "filename": filename,
                    "filepath": filepath,
                    "width": width,
                    "height": height,
                    "orientation": get_orientation(width, height),
                    "hero_eligible": max(width, height) >= 1200
                })
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

    if not pil_images:
        return []

    print(f"Loading CLIP model '{model_name}' on CPU")
    model = SentenceTransformer(model_name, device="cpu")

    print(f"Encoding {len(pil_images)} images into semantic vectors...")
    vectors = model.encode(
        pil_images,
        batch_size=batch_size,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    results = []
    for meta, vec in zip(metadata_list, vectors):
        results.append({
            **meta,
            "vector": np.array(vec, dtype=np.float32)
        })

    return results


if __name__ == "__main__":
    data = process_folder("images")
    print(f"\nSuccessfully processed {len(data)} images with CLIP.\n")
