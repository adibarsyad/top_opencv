import pymem

pm = pymem.Pymem("Game.exe")
hp_address = 0x09F4A840  # Replace with real HP address

while True:
    hp = pm.read_int(hp_address)
    print(f"Current HP: {hp}")