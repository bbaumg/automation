#!/usr/bin/env python

#  Call all of the imports
import time
import random
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

def halloween(strip):
	orange(strip)
	delay = random.randint(60,90)
	count = random.randint(3,7)
	logger.debug("The random delay is = " + str(delay))
	logger.debug("The strobe count is = " + str(count))
	time.sleep(delay)
	for _ in range(count):
		white(strip)
		time.sleep(.04)
		off(strip)
		time.sleep(.04)
	orange(strip)

def strobe(strip):
	for _ in range(100):
		white(strip)
		time.sleep(.05)
		off(strip)
		time.sleep(.05)

def off(strip):
        for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(0,0,0))
        strip.show()

def red(strip):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,255,0))
	strip.show()

def green(strip):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(255,0,0))
	strip.show()

def blue(strip):
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, Color(0,0,255))
	strip.show()

def white(strip):
        for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(255,255,255))
        strip.show()

def orange(strip):
        for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(55,255,0))
        strip.show()




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
  
  logger.critical("LED Startup Process")
  logger.critical("Starting RED")
  red(strip)
  time.sleep(1)
  logger.critical("Starting GREEN")
  green(strip)
  time.sleep(1)
  logger.critical("Starting BLUE")
  blue(strip)
  time.sleep(1)
  logger.critical("Starting WHITE")
  white(strip)
  time.sleep(1)

  


  logger.info("Beginning main loop")
  try:
	while True: # The main loop that will never end
		#rainbow(strip)
		halloween(strip)
		#strobe(strip)
		time.sleep(1)
		logger.debug("Bottom of Main Loop")
  except:
    logger.error("Writing Sensor Data = Unexpected error!")
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


  logging.shutdown()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
