#!/bin/bash
set -e

# Paths to local files
CONFIG_PATH="global.config.json"
IONINSTALLER_PATH="ioninstaller.sh"
GIT_REPO_URL="https://github.com/ice-blockchain/ion-controller.git"
GIT_BRANCH="ion-fork-rebase"

# Check if the script is run as root
if [ "$(id -u)" != "0" ]; then
    echo "Please run script as root"
    exit 1
fi

show_help_and_exit() {
    echo 'Supported arguments:'
    echo ' -m [lite|full]   Choose installation mode'
    echo ' -c  PATH         Provide custom config for ioninstaller.sh'
    echo ' -t               Disable telemetry'
    echo ' -i               Ignore minimum requirements'
    echo ' -d               Use pre-packaged dump. Reduces duration of initial synchronization.'
    echo ' -h               Show this help'
    exit
}

if [[ "${1-}" =~ ^-*h(elp)?$ ]]; then
    show_help_and_exit
fi

# Default arguments
config="$CONFIG_PATH"
telemetry=true
ignore=false
dump=false

# Parse arguments
while getopts m:c:tidh flag
do
    case "${flag}" in
        m) mode=${OPTARG};;
        c) config=${OPTARG};;
        t) telemetry=false;;
        i) ignore=true;;
        d) dump=true;;
        h) show_help_and_exit;;
        *)
            echo "Flag -${flag} is not recognized. Aborting"
            exit 1 ;;
    esac
done

# Check installation mode
if [ "${mode}" != "lite" ] && [ "${mode}" != "full" ]; then
    echo "Run script with flag '-m lite' or '-m full'"
    exit 1
else
    echo "Installation mode is ${mode}"
fi

# Check system resources
cpus=$(lscpu | grep "CPU(s)" | head -n 1 | awk '{print $2}')
memory=$(grep MemTotal /proc/meminfo | awk '{print $2}')
if [ "${mode}" = "lite" ] && [ "$ignore" = false ] && ([ "${cpus}" -lt 2 ] || [ "${memory}" -lt 2000000 ]); then
    echo "Insufficient resources for lite mode. Requires a minimum of 2 processors and 2Gb RAM."
    exit 1
else
    echo "Sufficient resources for lite mode or ignoring check."
fi

if [ "${mode}" = "full" ] && [ "$ignore" = false ] && ([ "${cpus}" -lt 8 ] || [ "${memory}" -lt 8000000 ]); then
    echo "Insufficient resources for full mode. Requires a minimum of 8 processors and 8Gb RAM."
    exit 1
else
    echo "Sufficient resources for full mode or ignoring check."
fi

# Colors for output
COLOR='\033[92m'
ENDC='\033[0m'

# Start installation message
echo -e "${COLOR}[1/4]${ENDC} Starting installation Ion-Controller"
mydir=$(pwd)

# Directories setup
SOURCES_DIR=/usr/src
BIN_DIR=/usr/bin
if [[ "$OSTYPE" =~ darwin.* ]]; then
    SOURCES_DIR=/usr/local/src
    BIN_DIR=/usr/local/bin
    mkdir -p ${SOURCES_DIR}
    echo "Running on OSX, directories adjusted."
else
    echo "Running on Linux."
fi

# Check for required ION components
echo -e "${COLOR}[2/4]${ENDC} Checking for required ION components"
file1=${BIN_DIR}/ion/crypto/fift
file2=${BIN_DIR}/ion/lite-client/lite-client
file3=${BIN_DIR}/ion/validator-engine-console/validator-engine-console
if [ -f "${file1}" ] && [ -f "${file2}" ] && [ -f "${file3}" ]; then
    echo "ION components exist."
    cd $SOURCES_DIR
    rm -rf $SOURCES_DIR/ion-controller
    git clone -b ${GIT_BRANCH} --recursive ${GIT_REPO_URL}
else
    echo "ION components do not exist. Running local ioninstaller.sh."
    bash ${IONINSTALLER_PATH} -c "${config}"
fi

# Run the myioninstaller.py script
echo -e "${COLOR}[3/4]${ENDC} Launching the myioninstaller.py"
parent_name=$(ps -p $PPID -o comm=)
user=$(whoami)
if [ "$parent_name" = "sudo" ] || [ "$parent_name" = "su" ]; then
    user=$(logname)
fi
echo "Running myioninstaller.py as user ${user} in mode ${mode}."
python3 ${SOURCES_DIR}/ion-controller/myioninstaller.py -m ${mode} -u ${user}

# Completion message
echo -e "${COLOR}[4/4]${ENDC} Ion-Controller installation completed"
exit 0
