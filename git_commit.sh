#!/bin/bash
echo **************************************************************
date
cd /home/pi/automation
git add .
git commit -m 'upload'
git push
date
