#!/bin/bash
full=true
while getopts f flag; do
	case "${flag}" in
		f) full=false
	esac
done

# Проверить sudo
if [ "$(id -u)" != "0" ]; then
	echo "Please run script as root"
	exit 1
fi

# Цвета
COLOR='\033[34m'
ENDC='\033[0m'

# Остановка служб
systemctl stop validator
systemctl stop myioncore
systemctl stop dht-server

# Переменные
str=$(systemctl cat myioncore | grep User | cut -d '=' -f2)
user=$(echo ${str})

# Удаление служб
rm -rf /etc/systemd/system/validator.service
rm -rf /etc/systemd/system/myioncore.service
rm -rf /etc/systemd/system/dht-server.service
systemctl daemon-reload

# Удаление файлов
if $full; then
	echo "removing Ion node"
	rm -rf /usr/src/ion
	rm -rf /usr/bin/ion
	rm -rf /usr/bin/fift
	rm -rf /usr/bin/liteclient
	rm -rf /usr/bin/lite-client
	rm -rf /usr/bin/myionctrl
	rm -rf /usr/bin/validator-console
	rm -rf /usr/local/bin/myioncore
	rm -rf /tmp/myion*
	rm -rf /var/ion-work
	rm -rf /var/ion-dht-server
fi

rm -rf /usr/src/ion-controller
rm -rf /usr/src/mtc-jsonrpc
rm -rf /usr/src/pytonv3

# removing pip packages
pip3 uninstall -y mytonctrl
pip3 uninstall -y ton-http-api

# Конец
echo -e "${COLOR}Uninstall Complete${ENDC}"
