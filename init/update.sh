#!/bin/bash

echo "setting permissions and user on main.py"
chown pi:pi /home/pi/automation/main.py
chmod 755 /home/pi/automation/main.py
echo "Installing init.d file"
cp -f /home/pi/automation/init/automation /etc/init.d/automation
chmod 777 /etc/init.d/automation 
chown root:root /etc/init.d/automation
echo "set start on boot and being first time"
update-rc.d automation defaults
service automation restart
echo "init script has been installed"
