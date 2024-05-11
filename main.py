# Roboverse Project
# Invisibility Cloak

import cv2
import numpy as np
import time

# Dictionary to hold HSV color ranges for different colors
color_ranges = {
    "red": {
        "lower": np.array([0, 100, 100]),
        "upper": np.array([10, 255, 255])
    },
    "orange": {
        "lower": np.array([10, 100, 100]),
        "upper": np.array([20, 255, 255])
    },
    "yellow": {
        "lower": np.array([20, 100, 100]),
        "upper": np.array([30, 255, 255])
    },
    "green": {
        "lower": np.array([30, 100, 100]),
        "upper": np.array([60, 255, 255])
    },
    "blue": {
        "lower": np.array([100, 100, 100]),
        "upper": np.array([140, 255, 255])
    },
    "indigo": {
        "lower": np.array([120, 100, 100]),
        "upper": np.array([140, 255, 255])
    },
    "violet": {
        "lower": np.array([140, 100, 100]),
        "upper": np.array([160, 255, 255])
    }
}

# Function to apply color detection and masking
def apply_color_mask(frame, color):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_range = color_ranges[color]["lower"]
    upper_range = color_ranges[color]["upper"]
    mask = cv2.inRange(hsv_frame, lower_range, upper_range)
    return mask

# Capturing video from the default camera
capture_video = cv2.VideoCapture(0)

# Allowing the camera to warm up for stability
time.sleep(1)

# Capturing 60 frames to set the background
for i in range(60):
    ret, background = capture_video.read()
    if not ret:
        continue

# Flipping the background because the camera's output is mirrored
background = np.flip(background, axis=1)

# Main loop for processing the video stream
while (capture_video.isOpened()):
    ret, img = capture_video.read()
    if not ret:
        break

    # Flipping the current frame (background + moving object)
    img = np.flip(img, axis=1)
    
    # Applying color detection and masking for red color
    mask = apply_color_mask(img, "green")

    # Applying morphological operations on the mask for better accuracy
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=2)

    # Creating a mask for the inverse of the main mask
    Nmask = cv2.bitwise_not(mask)

    # Segmentation of the foreground (person) and background
    res1 = cv2.bitwise_and(background, background, mask=mask)
    res2 = cv2.bitwise_and(img, img, mask=Nmask)

    # Blending both images with equal weight to maintain intensity
    output = cv2.addWeighted(res1, 1, res2, 1, 0)

    # Displaying the result
    cv2.imshow("Invisibility Cloak", output)
    
    # Exiting when 'Esc' key is pressed
    if cv2.waitKey(1) & 0xff == 27:
        break

# Releasing the camera and closing all OpenCV windows
cv2.destroyAllWindows()
