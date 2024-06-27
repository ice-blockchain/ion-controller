#!/bin/bash

# Show help and exit function
show_help_and_exit() {
    echo 'Usage: manage_ion.sh [OPTIONS]'
    echo 'Perform various operations for Ion controller management.'
    echo ''
    echo 'Options:'
    echo ' -i [install_ion_args]    Run install.sh as root with optional arguments'
    echo ' -f [install_ion_params]  Run install_with_config_params.sh as root with optional arguments'
    echo ' -c                       Run myionctrl.py from /usr/src/ion-controller'
    echo ' -u <backup_folder> <original_config>  Pause validator, move folders, and update config'
    echo ' -h                       Show this help message and exit'
    exit 1
}

# Check if no arguments were passed and show help
if [ $# -eq 0 ]; then
    show_help_and_exit
fi

# Initialize variables
run_install=false
run_install_params=false
run_myionctrl=false
pause_validator=false
install_ion_args=""
install_ion_params=""
backup_folder=""
original_config=""

# Parse arguments
while getopts "ifcu:h" flag; do
    case "${flag}" in
        i) run_install=true
           shift
           install_ion_args="$@"
           break
           ;;
        f) run_install_params=true
           shift
           install_ion_params="$@"
           break
           ;;
        c) run_myionctrl=true;;
        u) pause_validator=true
           backup_folder=$OPTARG
           original_config=$2
           shift 2;;
        h) show_help_and_exit;;
        *) echo "Invalid option: -${flag}" >&2; show_help_and_exit;;
    esac
done

# Function to run install.sh as root
run_install() {
    echo "Running install.sh as root with arguments: ${install_ion_args}"
    if [ "$(id -u)" != "0" ]; then
        echo "Please run this script as root to execute install.sh"
        exit 1
    fi
    ./install.sh ${install_ion_args}
}

# Function to run install_with_config_params.sh as root
run_install_with_config_params() {
    echo "Running install_with_config_params.sh as root with arguments: ${install_ion_params}"
    if [ "$(id -u)" != "0" ]; then
        echo "Please run this script as root to execute install_with_config_params.sh"
        exit 1
    fi
    ./install_with_config_params.sh ${install_ion_params}
}

# Function to run myionctrl.py from /usr/src/ion-controller
run_myionctrl() {
    echo "Running myionctrl.py from /usr/src/ion-controller..."
    cd /usr/src/ion-controller || { echo "Directory /usr/src/ion-controller does not exist."; exit 1; }
    python3 myionctrl.py
}

# Function to pause validator, move folders, and update config
pause_validator_and_move_folders() {
    echo "Pausing validator, moving folders, and updating config..."
    ./pause_validator_to_move_folders_and_update_config.sh -b "${backup_folder}" -o "${original_config}"
}

# Execute based on flags
if [ "${run_install}" = true ]; then
    run_install
fi

if [ "${run_install_params}" = true ]; then
    run_install_with_config_params
fi

if [ "${run_myionctrl}" = true ]; then
    run_myionctrl
fi

if [ "${pause_validator}" = true ]; then
    pause_validator_and_move_folders
fi
