import cv2
import numpy as np
import mss
import pyautogui

# Load the template (the uploaded object image)
template = cv2.imread("fishing_spot.png", cv2.IMREAD_UNCHANGED)
template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
w, h = template.shape[1], template.shape[0]

# Define the screen region to capture (Adjust for your game window)
monitor = {"top": 0, "left": 0, "width": 800, "height": 600}

def detect_and_click_object(frame):
    """Detects the object in the given frame using template matching."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Match the template in the screen capture
    result = cv2.matchTemplate(gray_frame, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.5  # Adjust sensitivity
    loc = np.where(result >= threshold)

    for pt in zip(*loc[::-1]):  # Iterate through detected points
      cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
      click_x = monitor["left"] + pt[0] + w // 2
      click_y = monitor["top"] + pt[1] + h // 2
      pyautogui.moveTo(click_x, click_y)
      pyautogui.press("f1")
      pyautogui.sleep(0.1)  # Small delay
      pyautogui.click()
      print(f"Clicked at: {click_x}, {click_y} - Waiting 15 seconds...")
      pyautogui.sleep(15)  # 900 seconds = 15 minutes

# Start real-time screen capture
with mss.mss() as sct:
    while True:
        # Capture the screen
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        # Detect and click on the object
        detect_and_click_object(frame)

        # Show the live detection output
        cv2.imshow("Object Detection", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
