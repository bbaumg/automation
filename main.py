#!/usr/bin/env python3

#  Call all of the imports
import time
import pymysql
import logging
#from neopixel import *

# Set all of the constants
cstlogFile = '/var/log/automation.log'
cstDBHost = 'localhost'
cstDBName = 'automation'
cstDBUser = 'automation'
cstDBPass = 'Pass1234'

# Setup logging
#logLevel = logging.CRITICAL
#logLevel = logging.ERROR
#logLevel = logging.WARNING
#logLevel = logging.INFO
logLevel = logging.DEBUG
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
      time.sleep(5)
      logger.debug("Bottom of Main Loop")
  except:
    logger.error("Unexpected error!")
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
