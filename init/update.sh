#!/bin/bash

cp -f /home/pi/automation/init/automation /etc/init.d/automation
sudo chmod 777 /etc/init.d/automation 
sudo chown root:root /etc/init.d/automation
sudo update-rc.d automation defaults
sudo /etc/init.d/automation start
echo "init scrip has been installed"
