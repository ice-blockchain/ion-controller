#!/bin/bash

# Check if the target directory is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <target_directory>"
    exit 1
fi

# Set the source and target directories
SOURCE_DIR="/var/ion-work/db"
TARGET_DIR="$1"

# List of folders to move
FOLDERS=("adnl" "archive" "catchains" "celldb" "files" "state" "overlays")

# Ensure the target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Target directory does not exist. Creating it..."
    mkdir -p "$TARGET_DIR"
fi

# Move each folder
for FOLDER in "${FOLDERS[@]}"; do
    if [ -d "$SOURCE_DIR/$FOLDER" ]; then
        echo "Moving $FOLDER to $TARGET_DIR"
        mv "$SOURCE_DIR/$FOLDER" "$TARGET_DIR"
    else
        echo "Folder $FOLDER does not exist in $SOURCE_DIR"
    fi
done

echo "All specified folders have been moved."
