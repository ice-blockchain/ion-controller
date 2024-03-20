#!/bin/bash

# Define the source directory
SOURCE_DIR="/var/ion-work/db"

# Define the backup directory (change this to your desired backup location)
BACKUP_DIR="/var/ion-work/dumps/"

# Create a timestamp for the backup file
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

# Define the name of the archive file
ARCHIVE_NAME="dump_${TIMESTAMP}.tar.gz"

# List of directories to archive
DIRS="adnl archive catchains celldb files state overlays"

# Change to the source directory
cd "$SOURCE_DIR"

# Stop validator-engine
systemctl stop validator

# Archive the specified directories
tar -czf "${BACKUP_DIR}/${ARCHIVE_NAME}" $DIRS

# Check if the tar command was successful
if [ $? -eq 0 ]; then
    echo "Backup successful: ${BACKUP_DIR}/${ARCHIVE_NAME}"
else
    echo "Backup failed"
fi

# Start validator-engine
systemctl start validator