import os
import shutil
import subprocess
import tarfile

def restore_dump_service(dump_url, db_dir="/var/ion-work/db"):
    # Stop validator-engine
    # subprocess.run(["systemctl", "stop", "validator"])

    # Create a fixed temporary directory for downloading the dump file
    temp_dir = "/tmp/restore_dump_temp"
    os.makedirs(temp_dir, exist_ok=True)
    dump_file = os.path.join(temp_dir, "dump_file.tar.gz")

    # Download the dump file using wget
    try:
        print(f"Running wget -O {dump_file} {dump_url}")
        subprocess.run(["wget", "-O", dump_file, dump_url], check=True)
        print(f"Downloaded dump file from {dump_url} to {dump_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download dump file: {e}")
        shutil.rmtree(temp_dir)
        return

    # List of directories to delete in the DB directory
    dirs_to_delete = ["adnl", "archive", "catchains", "celldb", "files", "state", "overlays"]

    # Delete each directory
    for dir_name in dirs_to_delete:
        dir_path = os.path.join(db_dir, dir_name)
        if os.path.isdir(dir_path):
            print(f"Deleting {dir_path}...")
            shutil.rmtree(dir_path)

    # Unzip the dump file into the DB directory
    try:
        with tarfile.open(dump_file, "r:gz") as tar:
            tar.extractall(path=db_dir)
        print(f"Restoration from {dump_file} to {db_dir} successful.")
    except Exception as e:
        print(f"Restoration failed: {e}")
        shutil.rmtree(temp_dir)
        return

    # Clean up temporary directory
    shutil.rmtree(temp_dir)
    print("Temporary files deleted.")
    print("Process completed.")

    # Start validator-engine
    # subprocess.run(["systemctl", "start", "validator"])

# Example usage
# restore_dump_service("http://example.com/path/to/dump_file.tar.gz")
if __name__ == "__main__":
    # URL of the dump file to download
    dump_url = "http://localhost:8000/dump_file.tar.gz"
    
    # Directory where the database should be restored
    db_dir = "/home/sabin/testpath/db_test"
    
    # Print a message indicating the start of the process
    print("Starting the database restoration process...")
    
    # Call the restore_dump_service function
    restore_dump_service(dump_url, db_dir)
    
    # Print a message indicating the end of the process
    print("Database restoration process completed.")