#!/usr/bin/env python3

#  Call all of the imports
import time
import math
import random
#import MySQLdb
import logging
from neopixel import *

# Set all of the constants
cstlogFile = '/var/log/automation.log'
cstDBHost = 'localhost'
cstDBName = 'automation'
cstDBUser = 'automation'
cstDBPass = 'Pass1234'

# LED strip configuration:
cstLEDCount   = 4      # Number of LED pixels.
cstLEDPin     = 18      # GPIO pin connected to the pixels (must support PWM!).
cstLEDFreqHZ  = 800000  # LED signal frequency in hertz (usually 800khz)
cstLEDDMA     = 5       # DMA channel to use for generating signal (try 5)
cstLEDInvert  = False   # True to invert the signal (when using NPN transistor level shift)

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

# Generate rainbow colors across 0-255 positions
#   pos = starting position
def wheel(pos):
	logger.info("Begin Function")
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

# Draw rainbow that fades across all pixels at once
#   strip = strip object defined at the beginning of the script
#   wait_ms = ?
#   iterations = ?
def rainbow(strip, wait_ms=50, iterations=1):
	logger.info("Begin Function")
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)
	logger.info("End Function")

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

# Used for halloween runs orange with randome lightning
#   strip = strip object defined at the beginning of the script
def halloween(strip):
	logger.info("Begin Function")
	setAllLEDs(strip,cOrange)
	delay = random.randint(60,90)
	count = random.randint(3,7)
	logger.debug("The random delay is = " + str(delay))
	logger.debug("The strobe count is = " + str(count))
	time.sleep(delay)
	for _ in range(count):
		setAllLEDs(strip,cWhite)
		time.sleep(.04)
		setAllLEDs(strip,cOff)
		time.sleep(.04)
	setAllLEDs(strip,cOrange)
	logger.info("End Function")

def july4th(strip):
  logger.info("Begin Function")
  colorWipe(strip, cRed, 2000)
  colorWipe(strip, cWhite, 2000)
  colorWipe(strip, cBlue, 2000)
  logger.info("End Function")

def july4th_v1(strip):
  logger.info("Begin Function")
  for p in range(0, cstLEDCount, 1):
    strip.setPixelColor(p, cRed)
    strip.setPixelColor(p+1, cWhite)
    strip.setPixelColor(p+2, cBlue)
    strip.show()
    time.sleep(1)
  logger.info("End Function")

# Continual white strobe
#   strip = strip object defined at the beginning of the script
def strobe(strip):
  logger.info("Begin Function")
  delay = 5
  logger.debug("Delay = " + str(delay))
  for _ in range(100):
    setAllLEDs(strip,cWhite)
    time.sleep(delay/100)
    setAllLEDs(strip,cOff)
    time.sleep(delay/100)
  logger.info("End Function")

# Set all LEDs to same color
def setAllLEDs(strip, varColor):
  logger.info("Begin Function")
  logger.info("Color = " + str(varColor))
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, varColor)
  strip.show()
  logger.info("End Function")

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
  strip = Adafruit_NeoPixel(cstLEDCount, cstLEDPin, cstLEDFreqHZ, cstLEDDMA, cstLEDInvert)
  strip.begin()
  
  # LED Color Codes
  logger.info("Set all base color codes")
  cOff    = Color(0,0,0)
  cRed    = Color(0,255,0)
  cGreen  = Color(255,0,0)
  cBlue   = Color(0,0,255)
  cWhite  = Color(255,255,255)
  cYellow = Color(255,255,10)
  cOrange = Color(55,255,0)
  cPurple = Color(0,75,130)
  cPink   = Color(21,255,133)
  july4th(strip)

  #~ logger.critical("LED Startup Process")
  #~ logger.critical("Starting RED")
  #~ setAllLEDs(strip,cRed)
  #~ time.sleep(.2)
  #~ logger.critical("Starting GREEN")
  #~ setAllLEDs(strip,cGreen)
  #~ time.sleep(.2)
  #~ logger.critical("Starting BLUE")
  #~ setAllLEDs(strip,cBlue)
  #~ time.sleep(.2)
  #~ logger.critical("Starting WHITE")
  #~ setAllLEDs(strip,cWhite)
  #~ time.sleep(.2)
  #~ logger.critical("wiping  RED")
  #~ colorWipe(strip, cRed)
  #~ logger.critical("wiping  GREEN")
  #~ colorWipe(strip, cGreen)
  #~ logger.critical("wiping  BLUE")
  #~ colorWipe(strip, cBlue)
  #~ logger.critical("wiping  WHITE")
  #~ colorWipe(strip, cWhite)
#~ 
  #~ logger.info("Beginning main loop")
  #try:
    #while True: # The main loop that will never end
      ##rainbow(strip)
      ##halloween(strip)
      ##strobe(strip)
      #july4th(strip)
      #time.sleep(1)
      #logger.debug("Bottom of Main Loop")
  #except:
    #logger.error("Writing Sensor Data = Unexpected error!")
    #logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


  #logging.shutdown()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
