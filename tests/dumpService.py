import os
import shutil
import subprocess
import tarfile
from datetime import datetime, timedelta
import time
import requests

def create_dump_service(source_dir, upload_url, period):
    period_delta = timedelta(seconds=period)
    
    while True:
        start_time = datetime.now()
        
        # Create a timestamp for the backup file
        TIMESTAMP = start_time.strftime("%Y-%m-%d_%H-%M-%S")

        # Define the name of the archive file
        ARCHIVE_NAME = f"dump_{TIMESTAMP}.tar.gz"
        LATEST_ARCHIVE_NAME = "dump_latest.tar.gz"

        # List of directories to archive
        DIRS = ["adnl", "archive", "catchains", "celldb", "files", "state", "overlays"]

        # Change to the source directory
        os.chdir(source_dir)

        # Stop validator-engine
        subprocess.run(["systemctl", "stop", "validator"], check=True)

        # Archive the specified directories
        archive_path = os.path.join("/tmp", ARCHIVE_NAME)
        latest_archive_path = os.path.join("/tmp", LATEST_ARCHIVE_NAME)
        try:
            with tarfile.open(archive_path, "w:gz") as tar:
                for dir_name in DIRS:
                    tar.add(dir_name)
            # Copy or rename the latest archive
            shutil.copyfile(archive_path, latest_archive_path)
            print(f"Backup successful: {archive_path} and updated {latest_archive_path}")
        except Exception as e:
            print(f"Backup failed: {e}")

        # Start validator-engine
        subprocess.run(["systemctl", "start", "validator"], check=True)

        # Upload the archive file to the specified URL
        try:
            with open(archive_path, 'rb') as f:
                response = requests.post(upload_url, files={'file': f})
            if response.status_code == 200:
                print(f"Upload successful: {upload_url}")
                os.remove(archive_path)  # Remove the file after successful upload
            else:
                print(f"Upload failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Upload failed: {e}")

        # Upload the latest archive file to the specified URL
        try:
            with open(latest_archive_path, 'rb') as f:
                response = requests.post(upload_url, files={'file': f})
            if response.status_code == 200:
                print(f"Upload of latest archive successful: {upload_url}")
            else:
                print(f"Upload of latest archive failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Upload of latest archive failed: {e}")

        # Calculate the next start time
        next_start_time = start_time + period_delta
        sleep_time = (next_start_time - datetime.now()).total_seconds()

        # Ensure we sleep only for a positive duration
        if sleep_time > 0:
            time.sleep(sleep_time)

def restore_dump_service(dump_url, db_dir):
    # Stop validator-engine
    subprocess.run(["systemctl", "stop", "validator"], check=True)

    # Define the name of the downloaded archive file
    archive_path = "/tmp/dump_restore.tar.gz"

    # Download the dump file from the specified URL
    try:
        response = requests.get(dump_url, stream=True)
        if response.status_code == 200:
            with open(archive_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Download successful: {archive_path}")
        else:
            print(f"Download failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"Download failed: {e}")
        return

    # List of directories to delete in the DB directory
    DIRS = ["adnl", "archive", "catchains", "celldb", "files", "state", "overlays"]

    # Navigate to the DB directory
    os.chdir(db_dir)

    # Delete each directory
    for dir_name in DIRS:
        dir_path = os.path.join(db_dir, dir_name)
        if os.path.isdir(dir_path):
            print(f"Deleting {dir_path}...")
            shutil.rmtree(dir_path)

    # Unzip the dump file into the DB directory
    print(f"Restoring from {archive_path} to {db_dir}...")
    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(db_dir)
        print("Restoration successful. Deleting the dump file...")
        os.remove(archive_path)
    except Exception as e:
        print(f"Restoration failed: {e}")

    print("Process completed.")

    # Start validator-engine
    subprocess.run(["systemctl", "start", "validator"], check=True)
