import requests
from datetime import datetime, timedelta
import tarfile
import shutil
import os
import subprocess
from time import sleep

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
#end define

