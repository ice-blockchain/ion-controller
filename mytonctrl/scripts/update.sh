#!/bin/bash
set -e

# Проверить sudo
if [ "$(id -u)" != "0" ]; then
	echo "Please run script as root"
	exit 1
fi

# Set default arguments
author="ion-blockchain"
repo="ion-controller"
branch="ion-fork"
srcdir="/usr/src/"
bindir="/usr/bin/"

# Get arguments
while getopts a:r:b: flag
do
	case "${flag}" in
		a) author=${OPTARG};;
		r) repo=${OPTARG};;
		b) branch=${OPTARG};;
	esac
done

# Цвета
COLOR='\033[92m'
ENDC='\033[0m'

# Go to work dir
cd ${srcdir}

# uninstall previous version
rm -rf ${srcdir}/${repo}
pip3 uninstall -y mytonctrl

# Update code
echo "https://github.com/${author}/${repo}.git -> ${branch}"
git clone --branch ${branch} --recursive https://github.com/${author}/${repo}.git
cd ${repo}
pip3 install -U .

systemctl daemon-reload

# Конец
echo -e "${COLOR}[1/1]${ENDC} Ion-Controller components update completed"
exit 0
