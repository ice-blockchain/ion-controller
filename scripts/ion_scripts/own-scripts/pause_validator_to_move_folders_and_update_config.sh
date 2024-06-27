#!/bin/bash

# Show help and exit function
show_help_and_exit() {
    echo 'Usage: manage_validator.sh [OPTIONS]'
    echo 'Perform operations to stop validator, move folders, and restart validator.'
    echo ''
    echo 'Options:'
    echo ' -b <backup_folder>       Path to the backup folder (required)'
    echo ' -o <original_config>     Path to the original global.config.json (required)'
    echo ' -h                       Show this help message and exit'
    exit 1
}

# Function to stop validator
stop_validator() {
    echo "Stopping validator service..."
    systemctl stop validator
}

# Function to empty the backup folder
empty_backup_folder() {
    local backup_folder=$1
    echo "Emptying backup folder: ${backup_folder}..."
    rm -rf "${backup_folder:?}/"*
}

# Function to move folders to the backup folder
move_folders() {
    local backup_folder=$1
    echo "Moving folders to backup folder..."
    ./move_folders.sh "${backup_folder}"
}

# Function to replace global.config.json
replace_config() {
    local original_config=$1
    local target_path="/usr/bin/ion/global.config.json"

    echo "Removing existing global.config.json from ${target_path}..."
    rm -f "${target_path}"

    echo "Copying global.config.json from ${original_config} to ${target_path}..."
    cp "${original_config}" "${target_path}"
}

# Function to restart validator
restart_validator() {
    echo "Restarting validator service..."
    systemctl restart validator
}

# Parse arguments
backup_folder=""
original_config=""
while getopts "b:o:h" flag; do
    case "${flag}" in
        b) backup_folder=${OPTARG};;
        o) original_config=${OPTARG};;
        h) show_help_and_exit;;
        *) echo "Invalid option: -${OPTARG}" >&2
           show_help_and_exit;;
    esac
done

# Check if required arguments are provided
if [ -z "${backup_folder}" ] || [ -z "${original_config}" ]; then
    echo "Error: Both backup folder and original config path are required."
    show_help_and_exit
fi

# Perform the tasks
stop_validator
empty_backup_folder "${backup_folder}"
move_folders "${backup_folder}"
replace_config "${original_config}"
restart_validator

echo "All operations completed successfully."
