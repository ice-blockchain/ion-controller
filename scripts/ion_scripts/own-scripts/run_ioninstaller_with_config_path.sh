#!/bin/bash

show_help_and_exit() {
    echo 'Usage: run_ioninstaller.sh -c <config_path> [OPTIONS]'
    echo 'Run ioninstaller.sh with the specified configuration file.'
    echo ''
    echo 'Options:'
    echo ' -c <config_path>   Path to the configuration file (required)'
    echo ' -h                 Show this help message and exit'
    exit 1
}

# Check if no arguments were passed and show help
if [ $# -eq 0 ]; then
    show_help_and_exit
fi

# Initialize variables
config_path=""
install_ion_args=""

# Parse arguments
while getopts "c:h" flag; do
    case "${flag}" in
        c) config_path=${OPTARG};;
        h) show_help_and_exit;;
        *) echo "Invalid option: -${OPTARG}" >&2
           show_help_and_exit;;
    esac
done

# Check if config_path is set
if [ -z "${config_path}" ]; then
    echo "Error: Configuration file path is required."
    show_help_and_exit
fi

# Additional arguments for ioninstaller.sh
shift $((OPTIND-1))
install_ion_args="$@"

# Function to run ioninstaller.sh with the specified configuration
run_ioninstaller() {
    local script_dir
    script_dir=$(dirname "$0")
    local ioninstaller_path="${script_dir}/ioninstaller.sh"

    echo "Running ioninstaller.sh with config: ${config_path} and arguments: ${install_ion_args}"
    if [ ! -f "${config_path}" ]; then
        echo "Error: Configuration file ${config_path} does not exist."
        exit 1
    fi

    if [ ! -f "${ioninstaller_path}" ]; then
        echo "Error: ioninstaller.sh not found in the same directory as run_ioninstaller.sh"
        exit 1
    fi

    bash "${ioninstaller_path}" -c "${config_path}" ${install_ion_args}
}

# Run the ioninstaller with the provided configuration path
run_ioninstaller
