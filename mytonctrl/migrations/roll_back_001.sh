pip3 uninstall -y mytonctrl

cd /usr/src
rm -rf myionctrl
git clone --recursive -b ion-fork https://github.com/ice-blockchain/ion-controller

echo "Updating /usr/bin/myionctrl"
echo "/usr/bin/python3 /usr/src/ion-controller/myionctrl.py $@" > /usr/bin/myionctrl
chmod +x /usr/bin/myionctrl

echo "Updating mytoncore service"
sed -i 's\-m mytoncore\/usr/src/ion-controller/myioncore.py\g' /etc/systemd/system/myioncore.service
systemctl daemon-reload
systemctl restart mytoncore

echo "Done"
