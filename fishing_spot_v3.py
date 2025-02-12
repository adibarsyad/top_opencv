import cv2
import numpy as np
import pyautogui
import mss
import time

# Load the template (Fishing Spot image)
template = cv2.imread("fishing_spot.png", cv2.IMREAD_UNCHANGED)  # Ensure it's loaded as a color image
if template is None:
    print("Error: Could not load fishing_spot.png")
    exit(1)

# Convert template to grayscale
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
h, w = template_gray.shape[:2]

# Define screen capture area (adjust based on your game window)
monitor = {"top": 100, "left": 100, "width": 1000, "height": 800}  # Adjust for your screen size

# Start screen capture loop
with mss.mss() as sct:
    while True:
        # Capture the screen
        screenshot = np.array(sct.grab(monitor))
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)  # Remove alpha channel if present

        # Convert screenshot to grayscale
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        # Match the template in the screenshot
        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Adjust this if needed
        loc = np.where(result >= threshold)

        if len(loc[0]) > 0:  # If at least one match is found
            max_val = np.max(result)
            print(f"Detected Fishing Spot with {max_val * 100:.2f}% similarity.")

            for pt in zip(*loc[::-1]):  # Iterate through detected points
                # Draw rectangle around detected fishing spot
                cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

                # Move the mouse to the detected position
                click_x = monitor["left"] + pt[0] + w // 2
                click_y = monitor["top"] + pt[1] + h // 2
                pyautogui.moveTo(click_x, click_y)

                # Press F1
                pyautogui.press('f1')

                # Wait 0.1 seconds
                time.sleep(0.1)

                # Right-click on the detected area
                pyautogui.rightClick()

                # Wait for 15 seconds before detecting again
                print("Waiting for 15 seconds before next detection...")
                time.sleep(15)
                break  # Stop after one detection to avoid clicking multiple times

        # Show detection window
        cv2.imshow("Fishing Spot Detection", screenshot)

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
