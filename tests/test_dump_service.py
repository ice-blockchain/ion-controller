import os
import shutil
import requests
from threading import Thread
from time import sleep

# Import the functions
from dumpService import create_dump_service, restore_dump_service

# Directory setup for testing
TEST_SOURCE_DIR = "/tmp/test_source_dir"
TEST_DB_DIR = "/tmp/test_db_dir"
TEST_UPLOAD_URL = "http://127.0.0.1:5000/upload"
TEST_DUMP_URL = "http://127.0.0.1:5000/uploads/dump_latest.tar.gz"
TEST_PERIOD = 10  # Short period for testing

# Helper function to setup test directories
def setup_test_directories():
    os.makedirs(TEST_SOURCE_DIR, exist_ok=True)
    os.makedirs(TEST_DB_DIR, exist_ok=True)

    # Create dummy files in the source directory
    for dir_name in ["adnl", "archive", "catchains", "celldb", "files", "state", "overlays"]:
        dir_path = os.path.join(TEST_SOURCE_DIR, dir_name)
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, "dummy_file.txt"), "w") as f:
            f.write("This is a test file.")

# Helper function to clean up test directories
def clean_up_test_directories():
    shutil.rmtree(TEST_SOURCE_DIR, ignore_errors=True)
    shutil.rmtree(TEST_DB_DIR, ignore_errors=True)

# Function to run create_dump_service in a separate thread
def run_create_dump_service():
    create_dump_service(TEST_SOURCE_DIR, TEST_UPLOAD_URL, TEST_PERIOD)

# Function to run restore_dump_service
def run_restore_dump_service():
    restore_dump_service(TEST_DUMP_URL, TEST_DB_DIR)

# Setup test environment
setup_test_directories()

# Run create_dump_service in a separate thread
thread = Thread(target=run_create_dump_service)
thread.start()

# Allow some time for the dump to be created and uploaded
sleep(TEST_PERIOD * 2)

# Run restore_dump_service
run_restore_dump_service()

# Verify restoration
restored_files_exist = all(
    os.path.exists(os.path.join(TEST_DB_DIR, dir_name, "dummy_file.txt"))
    for dir_name in ["adnl", "archive", "catchains", "celldb", "files", "state", "overlays"]
)

print("Restored files exist:", restored_files_exist)

# Clean up test environment
thread.join()
clean_up_test_directories()

# Check if the restored files exist in the destination directory
if restored_files_exist:
    print("Test passed: Restored files exist in the DB directory.")
else:
    print("Test failed: Restored files do not exist in the DB directory.")
