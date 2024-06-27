#!/bin/bash

show_help_and_exit() {
    echo 'Usage: manage_ion.sh [OPTIONS]'
    echo 'Run install_ion.sh or myionctrl.py based on provided flags.'
    echo ''
    echo 'Options:'
    echo ' -i [install_ion_args]    Run install_ion.sh as root with optional arguments'
    echo ' -c                       Run myionctrl.py from /usr/src/ion-controller'
    echo ' -h                       Show this help message and exit'
    exit 1
}

# Check if no arguments were passed and show help
if [ $# -eq 0 ]; then
    show_help_and_exit
fi

# Initialize variables
run_install=false
run_myionctrl=false
install_ion_args=""

# Parse arguments
while getopts "ich" flag; do
    case "${flag}" in
        i) run_install=true
           shift
           install_ion_args="$@"
           break
           ;;
        c) run_myionctrl=true;;
        h) show_help_and_exit;;
        *) echo "Invalid option: -${OPTARG}" >&2
           show_help_and_exit;;
    esac
done

# Function to run install_ion.sh as root
run_install_ion() {
    echo "Running install_ion_4_config_params.sh as root with arguments: ${install_ion_args}"
    if [ "$(id -u)" != "0" ]; then
        echo "Please run this script as root to execute install_ion.sh"
        exit 1
    fi
    install_ion_4_config_params.sh ${install_ion_args} # Adjust the path to your actual script location
}

# Function to run myionctrl.py from /usr/src/ion-controller
run_myionctrl() {
    echo "Running myionctrl.py from /usr/src/ion-controller..."
    cd /usr/src/ion-controller || { echo "Directory /usr/src/ion-controller does not exist."; exit 1; }
    python3 myionctrl.py
}

# Execute based on flags
if [ "${run_install}" = true ]; then
    run_install_ion
fi

if [ "${run_myionctrl}" = true ]; then
    run_myionctrl
fi
