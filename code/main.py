import os
import sys
from to_upload import upload_file
from to_download import download_file
from to_scan import scan_file
from paths import INPUT_DIR, OUTPUT_DIR, CLOUD_DIR
from oauth.login import get_drive_service


def main():
    ### Login first
    if not get_drive_service():
        print("Login failed")
        return

    while True:
        print("\nChoose an action:")
        print("u - Upload a file")
        print("d - Download a file")
        print("s - Scan a file")
        print("q - Quit")

        choice = input("Enter your choice (u/d/s/q): ").lower().strip()

        ### Upload a file
        if choice == 'u':
            if os.path.exists(INPUT_DIR):
                files = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f))]
                for file in files:
                    local_path = os.path.join(INPUT_DIR, file)
                    upload_file(local_path, CLOUD_DIR)
            else:
                print("Inputs directory not found")

        ### Download a file
        elif choice == 'd':
            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)
            download_file(CLOUD_DIR, OUTPUT_DIR)

        ### Scan a file
        elif choice == 's':
            if os.path.exists(INPUT_DIR):
                files = [f for f in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, f))]
                for file in files:
                    local_path = os.path.join(INPUT_DIR, file)
                    scan_file(local_path)
            else:
                print("Inputs directory not found")

        ### Quit :(
        elif choice == 'q':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter u, d, s, or q.")


if __name__ == "__main__":
    main()
