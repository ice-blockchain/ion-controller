# Manage Ion Controller

This repository contains scripts to manage the Ion controller. The primary script, `manage_ion.sh`, orchestrates various tasks such as installation, running the Ion controller, and managing validator configurations.

## Scripts Overview

- **install.sh**: Installs Ion components based on the provided mode (`lite` or `full`).
- **install_with_config_params.sh**: Installs Ion components with additional configuration parameters.
- **run_ioninstaller_with_config_path.sh**: Runs the Ion installer with a specified configuration file.
- **pause_validator_to_move_folders_and_update_config.sh**: Pauses the validator, moves specific folders to a backup location, and updates the global configuration file.

## Usage

### manage_ion.sh

The `manage_ion.sh` script provides a convenient way to execute the other scripts. Below are the options you can use with `manage_ion.sh`.

```bash
Usage: manage_ion.sh [OPTIONS]
Perform various operations for Ion controller management.

Options:
 -i [install_ion_args]    Run install.sh as root with optional arguments
 -f [install_ion_params]  Run install_with_config_params.sh as root with optional arguments
 -c                       Run myionctrl.py from /usr/src/ion-controller
 -u <backup_folder> <original_config>  Pause validator, move folders, and update config
 -h                       Show this help message and exit


Examples

Run install.sh with arguments
sudo ./manage_ion.sh -i -m full -c /path/to/config

Run install_with_config_params.sh with arguments
sudo ./manage_ion.sh -f -m lite -c /path/to/config

Run myionctrl.py
sudo ./manage_ion.sh -c

Pause validator, move folders, and update config
sudo ./manage_ion.sh -u /path/to/backup /path/to/original_config.json

Detailed Script Descriptions

install.sh
This script installs the Ion components based on the specified mode (lite or full). It checks system resources and verifies if the required components are already installed.

install_with_config_params.sh
This script installs the Ion components with additional configuration parameters. It allows specifying a custom configuration file and other options to customize the installation.

run_ioninstaller_with_config_path.sh
This script runs the Ion installer with a specified configuration file. It ensures the provided configuration file exists and then executes the installer with the given options.

pause_validator_to_move_folders_and_update_config.sh
This script performs the following tasks:

Stops the validator service.
Empties the specified backup folder.
Moves specific folders (adnl, archive, catchains, celldb, files, state, overlays) to the backup folder.
Replaces the existing global configuration file with a new one from the specified path.
Restarts the validator service.
