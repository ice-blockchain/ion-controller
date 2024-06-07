import os
import shutil
import subprocess
import tarfile
from datetime import datetime, timedelta
import time

def create_dump_service(source_dir = "/var/ion-work/db", backup_dir = "/var/ion-work/backup", period = 86400):
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
        # subprocess.run(["systemctl", "stop", "validator"], check=True)

        # Archive the specified directories
        archive_path = os.path.join(backup_dir, ARCHIVE_NAME)
        latest_archive_path = os.path.join(backup_dir, LATEST_ARCHIVE_NAME)
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
        # subprocess.run(["systemctl", "start", "validator"], check=True)

        # Calculate the next start time
        next_start_time = start_time + period_delta
        sleep_time = (next_start_time - datetime.now()).total_seconds()

        # Ensure we sleep only for a positive duration
        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == "__main__":
    # Example usage: Adjust these values as needed
    source_dir = "/home/sabin/testpath/db"  # Ensure this directory exists and contains the expected subdirectories
    backup_dir = "/home/sabin/testpath/backup"  # Ensure this directory exists and is writable
    period = 10  # Run every period seconds
    create_dump_service(source_dir, backup_dir, period)
