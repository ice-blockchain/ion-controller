import os
import subprocess
import tarfile
from datetime import datetime

# Define the source directory
SOURCE_DIR = "/var/ion-work/db"

# Define the backup directory (change this to your desired backup location)
BACKUP_DIR = "/var/ion-work/dumps"

# Create a timestamp for the backup file
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Define the name of the archive file
ARCHIVE_NAME = f"dump_{TIMESTAMP}.tar.gz"

# List of directories to archive
DIRS = ["adnl", "archive", "catchains", "celldb", "files", "state", "overlays"]

# Change to the source directory
os.chdir(SOURCE_DIR)

# Stop validator-engine
subprocess.run(["systemctl", "stop", "validator"], check=True)

# Archive the specified directories
archive_path = os.path.join(BACKUP_DIR, ARCHIVE_NAME)
try:
    with tarfile.open(archive_path, "w:gz") as tar:
        for dir_name in DIRS:
            tar.add(dir_name)
    print(f"Backup successful: {archive_path}")
except Exception as e:
    print(f"Backup failed: {e}")

# Start validator-engine
subprocess.run(["systemctl", "start", "validator"], check=True)
