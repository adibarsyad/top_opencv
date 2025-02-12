import pyautogui
import pytesseract
from PIL import Image
import pygetwindow as gw

# Make sure pytesseract is installed and Tesseract is set up correctly
# If not, you can download it from https://github.com/tesseract-ocr/tesseract

# Function to search for a string within the game window
def search_string_in_game_window(window_title, target_string):
    # Get the game window
    game_windows = gw.getWindowsWithTitle("Sky Pirates Online - A New Era")
    if not game_windows:
    	print("Game window not found!")
    	return
    game_window = game_windows[0]
    
    # Take a screenshot of the entire game window
    screenshot = pyautogui.screenshot(region=(game_window.left, game_window.top, game_window.width, game_window.height))
    
    # Use pytesseract to extract text from the screenshot
    extracted_text = pytesseract.image_to_string(screenshot)
    
    # Search for the target string in the extracted text
    if target_string in extracted_text:
        print(f"Found the string '{target_string}' in the game window!")
    else:
        print(f"The string '{target_string}' was not found in the game window.")

# Example usage
if __name__ == "__main__":
    window_title = "Sky Pirates Online - A New Era"  # Replace with the actual game window title
    target_string = "Mud Monster"  # Replace with the string you're looking for
    search_string_in_game_window(window_title, target_string)
