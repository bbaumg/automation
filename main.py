#!/usr/bin/env python3

#  Call all of the imports
import time
import logging
import configparser
import subprocess
import os

# Set all of the constants
cstlogFile = '/var/log/automation.log'
configFile = '/home/pi/automation/config.ini'

# Read in settings from the config file
config = configparser.ConfigParser()
config.sections()
config.read(configFile)
config.sections()
logLevel = config['main']['logLevel']
program = config['main']['program']

# Setup logging
logging.basicConfig(
  level=logLevel, 
  format='%(asctime)s - %(levelno)s - %(funcName)s - %(message)s', 
  datefmt = '%Y-%m-%d %H:%M:%S',
  filename = cstlogFile)
logger = logging.getLogger(__name__)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END SETUP - BEGIN FUNCTIONS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END FUNCTIONS - BEGIN PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if __name__ == '__main__':
  logger.critical("*****************************************************")
  logger.critical("*")
  logger.critical("* Starting Program")
  logger.critical("*")
  logger.critical("*****************************************************")
  logger.critical("Log Level = " + str(logLevel))
  logger.info("Beginning main loop")
  try:
    while True: # The main loop that will never end
      #subprocess.call("/home/pi/automation/pyephem.py", shell=True)
      #import pyephem
      logger.debug("Loading LED Module")
      os.system('/home/pi/automation/led.py')
      time.sleep(1)
      logger.debug("Bottom of Main Loop")
  except:
    logger.error("Unexpected error!")
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
