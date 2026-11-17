import cv2
import os

def is_image_sharp(image_path, threshold):
  """Checks if an image is sharp using the Variance of the Laplacian.

  - threshold: Lower values mean more tolerance for blur. Standard is 100-150.
  """
  # Load the image
  image = cv2.imread(image_path)
  if image is None:
    print(f"Could not load image: {image_path}")
    return False, 0.0

  # Convert to grayscale (sharpness doesn't depend on color)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

  # Calculate Laplacian variance
  variance = cv2.Laplacian(gray, cv2.CV_64F).var()

  # Return True if it meets or exceeds the threshold
  is_sharp = variance >= threshold
  return is_sharp, variance

def create_sharp_folder(folder_save_path):
    """Creates a folder for sharp images if it doesn't exist."""
    sharp_folder_path = os.path.join(folder_save_path, "sharp_images")
    if not os.path.exists(sharp_folder_path):
        os.makedirs(sharp_folder_path)
    return sharp_folder_path


def process_images(folder_path, quality_threshold, save_folder_path):
    """Processes images in a folder, checks sharpness, and copies sharp images to a new folder."""

    for filename in os.listdir(folder_path):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(folder_path, filename)
            sharp, score = is_image_sharp(image_path, quality_threshold)
            print(f"Image: {filename} - Is sharp: {sharp} (Score: {score:.2f})")

            if sharp:
                # Copy the sharp image to the new folder
                new_image_path = os.path.join(save_folder_path, filename)
                os.system(f"cp {image_path} {new_image_path}")