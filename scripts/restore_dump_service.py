import os
import shutil
import subprocess
import tarfile

# Define the directory where the dump file is located
DUMP_DIR = "/var/ion-work"

# Define the directory where the archived folders are located
DB_DIR = "/var/ion-work/db"

# Stop validator-engine
subprocess.run(["systemctl", "stop", "validator"], check=True)

# Navigate to the dump directory
os.chdir(DUMP_DIR)

# Find the dump file based on the pattern
dump_files = [f for f in os.listdir(DUMP_DIR) if f.startswith("dump_") and f.endswith(".tar.gz")]
DUMP_FILE = dump_files[0] if dump_files else None

# Check if the dump file exists
if DUMP_FILE is None:
    print(f"No dump file found in {DUMP_DIR}.")
    exit(1)

print(f"Found dump file: {DUMP_FILE}")

# List of directories to delete in the DB directory
DIRS = ["adnl", "archive", "catchains", "celldb", "files", "state", "overlays"]

# Navigate to the DB directory
os.chdir(DB_DIR)

# Delete each directory
for dir_name in DIRS:
    dir_path = os.path.join(DB_DIR, dir_name)
    if os.path.isdir(dir_path):
        print(f"Deleting {dir_path}...")
        shutil.rmtree(dir_path)

# Navigate back to the dump directory
os.chdir(DUMP_DIR)

# Unzip the dump file into the DB directory
print(f"Restoring from {DUMP_FILE} to {DB_DIR}...")
with tarfile.open(DUMP_FILE, "r:gz") as tar:
    tar.extractall(DB_DIR)

# Check if the unzip operation was successful
if tarfile.is_tarfile(DUMP_FILE):
    print("Restoration successful. Deleting the dump file...")
    os.remove(DUMP_FILE)
else:
    print("Restoration failed.")
    exit(1)

print("Process completed.")

# Start validator-engine
subprocess.run(["systemctl", "start", "validator"], check=True)
