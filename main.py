from src.core.discovery import Core
import time

def display_menu():
    print("\n=== Device Menu ===")
    print("1. List available devices")
    print("2. Connect to device")
    print("3. Exit")
    return input("Select option: ")

if __name__ == "__main__":
    core = Core()
    core.send_discovery_response()
    core.start_discovery()


    print("Core started. Use menu to interact.")
    while True:
        try:
            choice = display_menu()
            if choice == "1":
                print("\nAvailable devices:")
                print(core.list_available_devices())
            elif choice == "2":
                print("\nAvailable devices:")
                print(core.list_available_devices())
                peer_idx = int(input("\nEnter device number to connect: ")) - 1
                if core.connect_to_peer(peer_idx):
                    print("Connection established!")
                else:
                    print("Invalid device selection")
            elif choice == "3":
                print("Shutting down...")
                break
        except KeyboardInterrupt:
            print("\nCore stopped.")
            break
        except Exception as e:
            print(f"Error: {e}")
