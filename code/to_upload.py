import io
import os
from typing import Optional
from oauth.login import get_drive_service
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseUpload
from utils import load_crypt_key, encrypt_bytes_from_file


def find_or_create_folder(folder_name):
    """Find folder by name or create it if it doesn't exist"""
    service = get_drive_service()

    results = service.files().list(
      q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
      fields="files(id, name)"
    ).execute()

    folders = results.get('files', [])
    if folders:
        return folders[0]['id']

    folder_metadata = {
      'name': folder_name,
      'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    print(f"Created folder '{folder_name}' with ID: {folder.get('id')}")
    return folder.get('id')


def upload_file(local_path, drive_folder_name=None):
    service = get_drive_service()
    file_metadata = {'name': local_path.split('/')[-1]}

    if drive_folder_name:
        folder_id = find_or_create_folder(drive_folder_name)
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(local_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"File uploaded. File ID: {file.get('id')}")


def encrypt_and_upload(local_path: str, drive_folder_name: Optional[str] = None) -> str:
    service = get_drive_service()
    key = load_crypt_key()

    # read+encrypt in memory
    ciphertext = encrypt_bytes_from_file(local_path, key)

    # prepare filename on drive
    base_name = os.path.basename(local_path)
    enc_name = base_name + ".enc"

    # prepare metadata & parent folder
    file_metadata = {"name": enc_name}
    if drive_folder_name:
        folder_id = find_or_create_folder(drive_folder_name)
        file_metadata["parents"] = [folder_id]

    # upload from BytesIO to avoid writing .enc locally
    fh = io.BytesIO(ciphertext)
    fh.seek(0)
    media = MediaIoBaseUpload(fh, mimetype="application/octet-stream", resumable=True)

    request = service.files().create(body=file_metadata, media_body=media, fields="id")
    response = None
    # resumable upload loop
    while True:
        status, response = request.next_chunk()
        if status:
            # status.progress() may be None for tiny files; print safe progress
            prog = int(status.progress() * 100) if status.progress() is not None else None
            if prog is not None:
                print(f"Upload {prog}%")
        if response:
            break

    file_id = response.get("id")
    print(f"Encrypted upload complete: {enc_name} (File ID: {file_id})")
    return file_id
