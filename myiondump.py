import os
import shutil
import subprocess
import tarfile
from datetime import datetime, timedelta
import time


def create_dump_service(source_dir, backup_dir, period, delete_old_dump):
    period_delta = timedelta(seconds=period)

    while True:
        start_time = datetime.now()

        # Create a timestamp for the backup file
        TIMESTAMP = start_time.strftime("%Y-%m-%d_%H-%M-%S")

        # Define the name of the archive file
        ARCHIVE_NAME = f"dump_{TIMESTAMP}.tar.gz"
        LATEST_ARCHIVE_NAME = "dump_latest.tar.gz"

        # List of directories to archive
        DIRS = ["adnl", "archive", "catchains", "celldb", "files", "state", "static", "overlays"]

        # Change to the source directory
        os.chdir(source_dir)

        # Stop validator-engine
        subprocess.run(["systemctl", "stop", "validator"], check=True)

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
        subprocess.run(["systemctl", "start", "validator"], check=True)

        if delete_old_dump:
            try:
                backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('dump_') and f.endswith('.tar.gz')])
                # Keep only the latest and the previous two backups
                for old_backup in backups[:-3]:
                    os.remove(os.path.join(backup_dir, old_backup))
                print("Old backups deleted.")
            except Exception as e:
                print(f"Error deleting old backups: {e}")

        # Calculate the next start time
        next_start_time = start_time + period_delta
        sleep_time = (next_start_time - datetime.now()).total_seconds()

        # Ensure we sleep only for a positive duration
        if sleep_time > 0:
            time.sleep(sleep_time)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create and manage backups.")
    parser.add_argument('source_dir', type=str, default="/var/ion-work/db", help="The source directory to back up.")
    parser.add_argument('backup_dir', type=str, default="/var/ion-work/backup", help="The directory to store backups.")
    parser.add_argument('period', type=int, default=3600, help="The period (in seconds) between backups.")
    parser.add_argument('--delete_old_dump', action='store_true', help="Delete old backups, keeping only the latest and the previous two.")

    args = parser.parse_args()

    create_dump_service(args.source_dir, args.backup_dir, args.period, args.delete_old_dump)
