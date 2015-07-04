#!/bin/bash

# Create the base log file
echo 'Creating initial log file'
logfile='/var/log/automation.log'
touch $logfile
chown root:root $logfile
chmod 777 $logfile

# Create git_update log
echo 'Creating initial git_commit log file'
gitlogfile='/var/log/git_commit.log'
touch $gitlogfile
chown pi:pi $gitlogfile
chmod 777 $gitlogfile

# Setup log rotate
echo 'Configuring logrotate...'
rotatefile='/etc/logrotate.d/automation'
echo -en "$logfile\n$gitlogfile\n"\
"{\n"\
"  rotate 4\n"\
"  weekly\n"\
"  compress\n"\
"  notifempty\n"\
"}\n" > $rotatefile
chown root:root $rotatefile
chmod 755 $rotatefile
echo -en "\n\n"
cat $rotatefile
echo -en "\n\n"

# Install and start daemon
bash /home/pi/automation/init/update.sh

# Automate git update
crontab -l > rootcrontab
echo -en "0 1 * * * bash /home/pi/automation/git_commit.sh >> /var/log/git_commit.log 2>&1\n" >> rootcrontab
crontab rootcrontab
rm -f rootcrontab

# Completed
echo "Installation Complete"
