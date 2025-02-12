import pyautogui
import pytesseract
import pygetwindow as gw
import time

# Make sure pytesseract is installed and Tesseract is set up correctly
# If not, you can download it from https://github.com/tesseract-ocr/tesseract

# Function to search for a string within the game window and left-click on it
def search_strings_in_game_window(window_title, target_strings):
    # Get the game window
    game_windows = gw.getWindowsWithTitle(window_title)
    if not game_windows:
        print("Game window not found!")
        return []
    game_window = game_windows[0]
    
    # Take a screenshot of the entire game window
    screenshot = pyautogui.screenshot(region=(game_window.left, game_window.top, game_window.width, game_window.height))
    
    # Use pytesseract to extract text and bounding boxes (for each character)
    extracted_text = pytesseract.image_to_string(screenshot)
    print(f"Extracted text: {extracted_text}")
    
    found_positions = []
    
    # Check if any of the target strings are found in the extracted text
    for target_string in target_strings:
        if target_string in extracted_text:
            print(f"Found the string '{target_string}' in the game window!")
            
            # Find bounding boxes of all characters in the image
            boxes = pytesseract.image_to_boxes(screenshot)
            
            # Iterate over each character and find the one that matches the target string
            for box in boxes.splitlines():
                b = box.split()
                if b[0] == target_string[0]:  # Match the first character in the target string
                    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
                    
                    # Convert coordinates to screen coordinates based on the game window position
                    x += game_window.left
                    y += game_window.top
                    found_positions.append((x, y))
                    break
    
    return found_positions

# Function to click between target strings
def click_between_targets(found_positions):
    if len(found_positions) >= 2:
        # Sort positions by their X-coordinate
        found_positions.sort()
        
        # Click in the middle between the two target positions
        mid_x = (found_positions[0][0] + found_positions[1][0]) // 2
        mid_y = (found_positions[0][1] + found_positions[1][1]) // 2
        
        print(f"Clicking between targets at ({mid_x}, {mid_y})")
        pyautogui.click(mid_x, mid_y)

# Main loop that searches for the strings, clicks between them, and presses Shift key
def main():
    window_title = "Sky Pirates Online - A New Era"  # Replace with the actual game window title
    target_strings = ["Mud Monster", "Vampire Bat", "Miner Mole"]  # List of target strings to search for
    
    while True:
        # Hold down the Shift key
        pyautogui.keyDown('shift')
        
        # Search for the target strings in the game window
        found_positions = search_strings_in_game_window(window_title, target_strings)
        
        # If at least two target strings are found, click between them
        if len(found_positions) >= 2:
            click_between_targets(found_positions)
        
        # Release Shift key after performing the click action
        #pyautogui.keyUp('shift')
        
        # Sleep for a short time before continuing the loop (adjust as needed)
        time.sleep(1)

if __name__ == "__main__":
    main()
