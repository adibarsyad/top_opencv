import pytesseract
import cv2
import pyautogui
import pygetwindow as gw
import numpy as np
import time

# Target monster names
target_strings = ["Mud Monster", "Vampire Bat", "Miner Mole"]

# Function to detect and click on the monsters
def detect_and_click_monsters():
    # Get the game window
    game_window = gw.getWindowsWithTitle("Sky Pirates Online - A New Era")
    if not game_window:
        print("Game window not found!")
        return
    game_window = game_window[0]

    # Capture the screen region of the game window
    screenshot = pyautogui.screenshot(region=(game_window.left, game_window.top, game_window.width, game_window.height))
    screenshot = np.array(screenshot)
    
    # Convert to grayscale and apply histogram equalization
    gray_image = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    gray_image = cv2.equalizeHist(gray_image)
    
    # Resize for faster OCR processing
    gray_image = cv2.resize(gray_image, (800, 600))

    # Use pytesseract to extract text and the position of the target strings
    extracted_text = pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT, config='--psm 6', timeout=30)

    for i, word in enumerate(extracted_text['text']):
        if word in target_strings:
            # Get the position of the detected word
            x, y, w, h = extracted_text['left'][i], extracted_text['top'][i], extracted_text['width'][i], extracted_text['height'][i]
            center_x = x + w // 2
            center_y = y + h // 2
            
            # Move the mouse to the target position and click
            pyautogui.moveTo(center_x + game_window.left, center_y + game_window.top)
            pyautogui.click()
            print(f"Found {word} at ({center_x + game_window.left}, {center_y + game_window.top}) and clicked!")
            
            # Sleep to give time for the monster to be removed from the screen
            time.sleep(1)

# Continuously search for the monsters and click
def main():
    while True:
        try:
            detect_and_click_monsters()
            time.sleep(0.1)  # Adjust sleep time to match your needs
        except KeyboardInterrupt:
            print("Process interrupted by the user.")
            break

if __name__ == "__main__":
    main()
