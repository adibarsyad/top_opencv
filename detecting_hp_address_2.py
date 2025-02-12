import pymem
import pymem.process
import re

def search_memory_for_value(process_name, value_to_search):
    # Attach to the game process
    pm = pymem.Pymem(process_name)
    
    # Get the list of loaded modules
    base_module = pymem.process.base_module(pm.process_handle)
    print(f"Base module: {base_module}")
    
    # Use base_module to get the base address of the main module
    region_base = base_module.lpBaseOfDll
    region_size = base_module.SizeOfImage
    
    # Read the entire memory region of the module
    try:
        memory_bytes = pm.read_bytes(region_base, region_size)
    except Exception as e:
        print(f"Failed to read memory region {hex(region_base)}: {e}")
        return
    
    # Search for the value in the memory region
    try:
        # If searching for an integer, use byte conversion
        if isinstance(value_to_search, int):
            value_bytes = value_to_search.to_bytes(4, byteorder='little')  # 4 bytes for an integer
        elif isinstance(value_to_search, str):
            value_bytes = value_to_search.encode('utf-8')  # Encoding string to bytes
        else:
            print("Unsupported search value type!")
            return
        
        # Find matches
        matches = memory_bytes.find(value_bytes)  # Find first occurrence
        while matches != -1:
            address = region_base + matches
            print(f"Found value {value_to_search} at address: {hex(address)}")
            matches = memory_bytes.find(value_bytes, matches + 1)  # Continue searching
    
    except Exception as e:
        print(f"Error during memory search: {e}")
        return

# Example usage
if __name__ == "__main__":
    process_name = "Game.exe"  # Replace with the game's process name
    value_to_search = 21662  # Replace with the value you're searching for (e.g., health)
    
    search_memory_for_value(process_name, value_to_search)
