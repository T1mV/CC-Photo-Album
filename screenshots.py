import cv2
import numpy as np
import os
from PIL import Image
import shutil

def is_screenshot_by_ui(image_path):
  """Detects screenshots by looking for top status bars and bottom navigation bars

  using edge and contour analysis.
  """
  image = cv2.imread(image_path)
  if image is None:
    return False

  height, width, _ = image.shape

  # 1. Check the top 7% (Status Bar area) and bottom 7% (Navigation bar area)
  top_strip = image[0 : int(height * 0.07), 0:width]
  bottom_strip = image[int(height * 0.93) : height, 0:width]

  for strip in [top_strip, bottom_strip]:
    gray = cv2.cvtColor(strip, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection to find crisp UI lines and icon shapes
    edges = cv2.Canny(gray, 50, 150)

    # Find horizontal lines or distinct clustered bounding boxes (common for status bar icons)
    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Count small sharp elements typical of wifi/battery icons or clock text
    ui_elements_count = 0
    for c in contours:
      x, y, w, h = cv2.boundingRect(c)
      # Status bar icons are typically small and clustered near the top/bottom edges
      if 5 < w < 60 and 5 < h < 30:
        ui_elements_count += 1

    # If we find multiple small UI-like icons packed into the top/bottom edge strip
    if ui_elements_count >= 4:
      return True

  return False

def is_screenshot(image_path):
  # Check 1: Does it have camera hardware EXIF data?
  try:
    with Image.open(image_path) as img:
      exif = img._getexif()
      if exif:
        # If it has a camera Make/Model tag, it's 100% a real photo, skip UI checks
        for tag_id, value in exif.items():
          if tag_id in [271, 272]:  # 271: Make, 272: Model
            return False
  except Exception:
    pass

  # Check 2: If no camera EXIF exists, run the UI status bar check
  return is_screenshot_by_ui(image_path)

def screenshots_folder(folder_path):
    non_screenshot_folder = os.path.join(folder_path, "non_screenshots")
    if not os.path.exists(non_screenshot_folder):
        os.makedirs(non_screenshot_folder)
    return non_screenshot_folder

def check_screenshots_in_folder(folder_path, non_screenshot_folder):
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if not os.path.isfile(image_path):
            continue
        screenshot_check = is_screenshot(image_path)
        #print(f"File: {filename}, Screenshot Check: {screenshot_check}")
        #if it not a screenshot, copy it to the non_screenshots folder
        
        if not screenshot_check:
            destination_path = os.path.join(non_screenshot_folder, filename)
            shutil.copy2(image_path, destination_path)
            #print(f"Copied {filename} to non_screenshots folder.")
    print("Finished non screenshot check and copying.")