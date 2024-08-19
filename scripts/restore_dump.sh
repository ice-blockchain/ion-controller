#!/bin/bash

# Define the directory where the dump file is located
DUMP_DIR="/var/ion-work"

# Define the directory where the archived folders are located
DB_DIR="/var/ion-work/db"

# Stop validator-engine
systemctl stop validator

# Navigate to the dump directory
cd "$DUMP_DIR"

# Find the dump file based on the pattern
DUMP_FILE=$(ls dump_*.tar.gz 2>/dev/null | head -n 1)

# Check if the dump file exists
if [ -z "$DUMP_FILE" ]; then
    echo "No dump file found in $DUMP_DIR."
    exit 1
fi

echo "Found dump file: $DUMP_FILE"

# List of directories to delete in the DB directory
DIRS=("adnl" "archive" "catchains" "celldb" "files" "state" "overlays")

# Navigate to the DB directory
cd "$DB_DIR"

# Delete each directory
for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "Deleting $DB_DIR/$dir..."
        rm -rf "$dir"
    fi
done

# Navigate back to the dump directory
cd "$DUMP_DIR"

# Unzip the dump file into the DB directory
echo "Restoring from $DUMP_FILE to $DB_DIR..."
tar -xzf "$DUMP_FILE" -C "$DB_DIR"

# Check if the unzip operation was successful
if [ $? -eq 0 ]; then
    echo "Restoration successful. Deleting the dump file..."
    rm -f "$DUMP_FILE"
else
    echo "Restoration failed."
    exit 1
fi

echo "Process completed."

# Start validator-engine
systemctl start validator
