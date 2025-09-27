import io
import os
from googleapiclient.http import MediaIoBaseDownload
from oauth.login import get_drive_service
from utils import load_crypt_key, decrypt_bytes_to_file
from paths import INPUT_DIR

def find_folder_by_name(folder_name):
    service = get_drive_service()

    results = service.files().list(
      q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
      fields="files(id, name)"
    ).execute()

    folders = results.get('files', [])
    if folders:
        return folders[0]['id']  # Return first matching folder ID
    return None


def download_file(folder_name, destination_dir):
    service = get_drive_service()

    # Find the folder
    folder_id = find_folder_by_name(folder_name)
    if not folder_id:
        print(f"Folder '{folder_name}' not found")
        return

    # List all files in the folder
    results = service.files().list(
      q=f"'{folder_id}' in parents and mimeType!='application/vnd.google-apps.folder'",
      fields="files(id, name)"
    ).execute()

    files = results.get('files', [])
    if not files:
        print(f"No files found in folder '{folder_name}'")
        return

    for file in files:
        file_id = file['id']
        file_name = file['name']
        destination_path = os.path.join(destination_dir, file_name)

        print(f"Downloading {file_name}...")
        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(destination_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
        print(f"File downloaded to {destination_path}")


def download_and_decrypt(folder_name: str, destination_dir: str = INPUT_DIR) -> None:
    service = get_drive_service()
    key = load_crypt_key()

    folder_id = find_folder_by_name(folder_name)
    if not folder_id:
        print(f"Folder '{folder_name}' not found on Drive.")
        return

    # list files (non-folders) in folder
    results = service.files().list(
      q=f"'{folder_id}' in parents and mimeType!='application/vnd.google-apps.folder'",
      fields="files(id, name)"
    ).execute()
    files = results.get("files", [])
    if not files:
        print(f"No files found in folder '{folder_name}'")
        return

    for fmeta in files:
        file_id = fmeta["id"]
        file_name = fmeta["name"]

        print(f"Downloading {file_name} (id={file_id}) ...")
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status and status.progress() is not None:
                print(f"Download {int(status.progress() * 100)}%")

        fh.seek(0)
        ciphertext = fh.read()

        if file_name.lower().endswith(".enc"):
            out_name = file_name[:-4]
        else:
            out_name = file_name + ".dec"

        out_path = os.path.join(destination_dir, out_name)

        try:
            decrypt_bytes_to_file(ciphertext, out_path, key)
            print(f"Decrypted and wrote: {out_path}")
        except ValueError as e:
            print(f"Failed to decrypt {file_name}: {e}")
