#!/bin/bash

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
rm -rf /usr/src/ion-controller
rm -rf /usr/src/ion
rm -rf /usr/bin/ion
rm -rf /var/ion-work
rm -rf /var/ion-dht-server
rm -rf /tmp/myion*
rm -rf /usr/local/bin/myioninstaller/
rm -rf /usr/local/bin/myioncore
rm -rf /home/${user}/.local/share/myionctrl
rm -rf /home/${user}/.local/share/myioncore/myioncore.db

# Удаление ссылок
rm -rf /usr/bin/fift
rm -rf /usr/bin/liteclient
rm -rf /usr/bin/lite-client
rm -rf /usr/bin/validator-console
rm -rf /usr/bin/myionctrl

# Конец
echo -e "${COLOR}Uninstall Complete${ENDC}"
