import pymem
import pymem.process

# Open the game process
pm = pymem.Pymem('Game.exe')

# Define the string to search for
search_string = "Fishing Spot"

# Function to scan for the specific string
def scan_for_string():
    # Scan all memory regions loaded by the game process
    for module in pm.list_modules():
        base_address = module.lpBaseOfDll
        module_size = module.SizeOfImage
        
        # Scan the module's memory for the string
        for address in range(base_address, base_address + module_size, 1024):  # Scan in chunks of 1024 bytes
            try:
                # Read a chunk of memory and convert to string
                memory_data = pm.read_bytes(address, 1024).decode('utf-8', errors='ignore')
                if search_string in memory_data:
                    print(f"Found '{search_string}' at address: 0x{address:X}")
            except Exception as e:
                # Ignore any exceptions caused by invalid memory reads
                continue

# Run the function to scan for the string
scan_for_string()
