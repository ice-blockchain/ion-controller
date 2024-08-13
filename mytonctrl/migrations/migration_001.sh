#!/bin/bash

# installing pip package
if [ -f "setup.py" ]; then 
    workdir=$(pwd)
else
    workdir=/usr/src/ion-controller
fi

cd $workdir
pip3 install -U pip .

# update /usr/bin/mytonctrl
echo "    Updating /usr/bin/myionctrl"
cat <<EOF > /usr/bin/myionctrl
#!/bin/bash
/usr/bin/python3 -m mytonctrl \$@
EOF
chmod +x /usr/bin/myionctrl

# update /etc/systemd/system/mytoncore.service
echo "    Updating myioncore service"
sed -i 's\/usr/src/ion-controller/myioncore.py\-m mytoncore\g' /etc/systemd/system/myioncore.service
systemctl daemon-reload
