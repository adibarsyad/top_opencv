import pymem
import time

def find_hp_address(process_name, scan_duration=60, max_results=10):
    try:
        pm = pymem.Pymem(process_name)
    except pymem.exception.CouldNotOpenProcess:
        print("❌ ERROR: Could not open process. Try running as Administrator.")
        return None

    print(f"✅ Attached to process: {process_name} (PID: {pm.process_id})")

    # Step 1: Print all loaded modules and find the one you need
    print("\n📜 Listing loaded modules in the game process:")
    for module in pm.list_modules():
        print(f"Module: {module.name}, Base Address: {hex(module.lpBaseOfDll)}, Size: {module.SizeOfImage}")

    # Get user input for HP value
    initial_hp = int(input("Enter your current HP: "))

    print(f"🔍 Scanning for memory addresses with HP value: {initial_hp} (Max {scan_duration} seconds)")

    possible_hp_addresses = []
    start_time = time.time()  # Track start time

    with open("hp_addresses.log", "w") as log_file:  # Open log file
        log_file.write(f"HP Scan Log - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Looking for HP: {initial_hp}\n\n")

        # Scan the specific module (igddxvacommon32.dll)
        for memory_page in pm.list_modules():
            if memory_page.name.lower() == "Game.exe":  # Focus on the igddxvacommon32.dll module
                base_address = memory_page.lpBaseOfDll
                size = memory_page.SizeOfImage

                for addr in range(base_address, base_address + size, 4):  # Step by 4 bytes
                    if time.time() - start_time > scan_duration:  # Stop if 1 min passes
                        print("⏳ Time limit reached! Stopping scan...")
                        break

                    try:
                        value = pm.read_int(addr)
                        if value == initial_hp:
                            possible_hp_addresses.append(addr)
                            log_file.write(f"Found HP Address: {hex(addr)}\n")  # Log to file
                            print(f"✅ Found HP Address: {hex(addr)}")

                            if len(possible_hp_addresses) >= max_results:  # Stop after 10 results
                                break
                    except:
                        pass

                if len(possible_hp_addresses) >= max_results or time.time() - start_time > scan_duration:
                    break  # Stop scanning

    if not possible_hp_addresses:
        print("❌ No matching HP values found. Try again.")
        return None

    print(f"✅ Found {len(possible_hp_addresses)} possible HP addresses (Saved to hp_addresses.log)")

    return possible_hp_addresses

# Run the script
process_name = "Game.exe"  # Change if needed
hp_addresses = find_hp_address(process_name)

if hp_addresses:
    print("\n🎯 Save one of these addresses for use in your bot!")
