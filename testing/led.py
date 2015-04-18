#!/usr/bin/env python

#  Call all of the imports
import time
import MySQLdb
import logging
from neopixel import *

# Set all of the constants
cstlogFile = '/var/automation/main.log'
cstDBHost = 'localhost'
cstDBName = 'automation'
cstDBUser = 'automation'
cstDBPass = 'Pass1234'

# LED strip configuration:
LED_COUNT   = 4      # Number of LED pixels.
LED_PIN     = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA     = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT  = False   # True to invert the signal (when using NPN transistor level shift)

# Setup logging
#logLevel = logging.CRITICAL
#logLevel = logging.ERROR
#logLevel = logging.WARNING
#logLevel = logging.INFO
logLevel = logging.DEBUG

#logLevel = DEBUG
logging.basicConfig(
  level=logLevel, 
  format='%(asctime)s - %(levelno)s - %(funcName)s - %(message)s', 
  datefmt = '%Y-%m-%d %H:%M:%S',
  filename = cstlogFile)
logger = logging.getLogger(__name__)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END SETUP - BEGIN FUNCTIONS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=50, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)


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
  logger.critical("Starting NeoPixel")
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
  strip.begin()
  
  logger.info("Beginning main loop")
  try:
	while True: # The main loop that will never end
		rainbow(strip)
		#strip.setPixelColor(0, Color(255,0,0))
                #strip.setPixelColor(1, Color(0,255,0))
                #strip.setPixelColor(2, Color(0,0,255))
                #strip.setPixelColor(3, Color(255,255,255))
                #strip.setPixelColor(4, Color(255,255,255))
                #strip.setPixelColor(5, Color(0,0,0))
		#strip.show()
		#time.sleep(5)
		logger.debug("Bottom of Main Loop")
  except:
    logger.error("Writing Sensor Data = Unexpected error!")
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


  logging.shutdown()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
