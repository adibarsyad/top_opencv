import cv2
import numpy as np
import pyautogui
import mss
import time

# Define the monitoring area for screen capture
monitor = {"top": 0, "left": 0, "width": 1000, "height": 1000}

# Load the template images (add your own paths)
templates = [
    ("monster1.png", cv2.imread("monster1.png", cv2.IMREAD_UNCHANGED)),
    ("monster2.png", cv2.imread("monster2.png", cv2.IMREAD_UNCHANGED)),
    ("monster3.png", cv2.imread("monster3.png", cv2.IMREAD_UNCHANGED)),
]

# Validate if templates are loaded correctly
for name, template in templates:
    if template is None:
        print(f"Error: Could not load template image {name}")
        exit(1)

# Start screen capture loop
with mss.mss() as sct:
    while True:
        # Capture the screen region
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

        for name, template in templates:
            h, w = template.shape[:2]

            # Match the template in the screenshot
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8  # Adjust if necessary
            loc = np.where(result >= threshold)

            for pt in zip(*loc[::-1]):  # Iterate through detected points
                # Draw a rectangle around detected object
                cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

                # Move and click on the detected object
                click_x = monitor["left"] + pt[0] + w // 2
                click_y = monitor["top"] + pt[1] + h // 2

                # Move cursor to detected object
                pyautogui.moveTo(click_x, click_y)

                # Click the detected monster
                pyautogui.click()

                # Wait 3-4 seconds before detecting the next monster
                wait_time = np.random.uniform(3, 4)
                print(f"Clicked {name} at: {click_x}, {click_y} - Waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)

        # Show the processed frame in a window
        cv2.imshow("Detection", screenshot)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
