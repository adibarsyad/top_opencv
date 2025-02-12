import pymem
import pyautogui
import pygetwindow as gw
import time
import random

# The address for the monster names in the memory (relative to Game.exe)
monster_name_address = 0x01011A35  # Replace with the correct memory offset
monster_names_to_check = ["Mud Monsterl Spirit", "Miner Molel Spirit", "Vampire Batl Spirit"]

# Function to read the monster name from memory
def read_monster_name(pm):
    try:
        # Read the memory at the given address (monster name)
        monster_name_bytes = pm.read_bytes(monster_name_address, 32)  # Adjust length if needed
        monster_name = monster_name_bytes.decode('utf-8').strip('\x00')
        return monster_name
    except Exception as e:
        print(f"Failed to read monster name: {e}")
        return None

# Function to simulate right-click
def right_click_on_screen():
    pyautogui.click(button='left')

# Function to move the mouse within the center region of the game window (200 pixel radius) and spam right-click
def move_and_right_click_spam(game_window, radius=200, clicks_per_second=5):
    # Get the window's position and size
    left, top, right, bottom = game_window.left, game_window.top, game_window.right, game_window.bottom
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2
    
    # Number of right-clicks to perform per second
    right_clicks = int(clicks_per_second)
    
    for _ in range(right_clicks):
        # Generate random coordinates within a circle of given radius around the center
        rand_x = random.randint(center_x - radius, center_x + radius)
        rand_y = random.randint(center_y - radius, center_y + radius)
        
        # Make sure the coordinates are within the game window bounds
        rand_x = max(min(rand_x, right), left)
        rand_y = max(min(rand_y, bottom), top)
        
        pyautogui.moveTo(rand_x, rand_y)
        right_click_on_screen()
        
        time.sleep(1 / clicks_per_second)  # Delay between right clicks to achieve speed

# Function to get the game window by process name
def get_game_window(process_name):
    try:
        # Get the window with the process name
        game_window = gw.getWindowsWithTitle(process_name)[0]
        return game_window
    except IndexError:
        print(f"Window with title '{process_name}' not found.")
        return None

# Main function to detect monster and right-click until the name is gone
def main():
    # Attach to the game process
    pm = pymem.Pymem("Game.exe")  # Replace with the correct process name
    
    # Get the game window
    game_window = get_game_window("Sky Pirates Online - A New Era")  # Replace with the actual game window title
    
    if game_window is None:
        print("Game window not found!")
        return
    
    while True:
        # Read the monster name from memory
        monster_name = read_monster_name(pm)
        
        if monster_name in monster_names_to_check:
            print(f"Found monster '{monster_name}', right-clicking...")
            move_and_right_click_spam(game_window)  # Spam right-clicks within the 200px radius
        else:
            print(f"Monster '{monster_name}' is gone or not found!")
        
        time.sleep(1)  # Sleep for a second before checking again

if __name__ == "__main__":
    main()
