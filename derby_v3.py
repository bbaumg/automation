#!/usr/bin/env python3

####################################################################
#  Pinewood derby timer and winner display software.
#  Written by:  Barrett Baumgartner
#  Purpose:  Keep track of a 4 lane Pinewood Derby track. Report 
#            rankings and completion time
####################################################################

import RPi.GPIO as GPIO
import sys
import time
import math
import signal
import logging
from datetime import datetime
from Adafruit_LED_Backpack import SevenSegment
from neopixel import *

# Setup logging
logging.basicConfig(
  level='CRITICAL', 
  format='%(asctime)s - %(levelno)s - %(funcName)s - %(message)s', 
  datefmt = '%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 22(PIN 15) Start
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 23(PIN 16) Lane 1
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 24(PIN 18) Lane 2
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 25(PIN 22) Lane 3
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO  4(PIN  7) Lane 4
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 27(PIN 13) Reset Switch

try:
  # Indicator LED Configuration:  Addressable Pixels
  cstLEDCount   = 4       # Number of LED pixels.
  cstLEDPin     = 18      # GPIO pin connected to the pixels (must support PWM!).
  cstLEDFreqHZ  = 800000  # LED signal frequency in hertz (usually 800khz)
  cstLEDDMA     = 5       # DMA channel to use for generating signal (try 5)
  cstLEDInvert  = False   # True to invert the signal (when using NPN transistor level shift)
  strip = Adafruit_NeoPixel(cstLEDCount, cstLEDPin, cstLEDFreqHZ, cstLEDDMA, cstLEDInvert)
  #~ strip.begin()
except:
  print("I guess it failed")

dispTimeL1 = SevenSegment.SevenSegment(address=0x70)
dispTimeL1.begin()
dispTimeL1.colon = False

dispTimeL2 = SevenSegment.SevenSegment(address=0x71)
dispTimeL2.begin()
dispTimeL2.colon = False

#~ dispTimeL3 = SevenSegment.SevenSegment(address=0x72)
#~ dispTimeL3.begin()
#~ dispTimeL3.colon = False

#~ dispTimeL4 = SevenSegment.SevenSegment(address=0x73)
#~ dispTimeL4.begin()
#~ dispTimeL4.colon = False

l1 = False
l2 = False
l3 = False
l4 = False

val_Lane2Disp = {1:0, 2:1, 3:3, 4:4}

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def raceStart(channel):
  global dt_RaceStart
  global p1
  global p2
  global p3
  global p4
  global l1
  global l2
  global l3
  global l4
  dt_RaceStart = datetime.now()
  print("Start of race = " + str(dt_RaceStart))
  #~ getRank("START")
  p1 = ""
  p2 = ""
  p3 = ""
  p4 = ""
  l1 = False
  l2 = False
  l3 = False
  l4 = False
  outResetDisp()

def lane1(channel):
  lane = 1
  global l1
  if l1 == True:
    print("That car already whent through")
  else:
    l1 = True
    processRace(lane)

def lane2(channel):
  lane = 2
  processRace(lane)

def lane3(channel):
  lane = 3
  processRace(lane)

def lane4(channel):
  lane = 4
  processRace(lane)

def processRace(lane):
  #~ print("Lane " + str(lane) + " = ")
  finishTime = getTime(lane)
  finishRank = getRank(lane)
  #~ print(finishTime)
  #~ print(finishRank)
  outTimeDisp(lane, finishTime)
  #~ print("End lane " + str(lane))

def getRank(lane):
  global p1
  global p2
  global p3
  global p4
   
  if p1 == "":
    p1 = lane
    rank = 1
    return 1
  elif p2 == "":
    p2 = lane
    rank = 2
    return 2
  elif p3 == "":
    p3 = lane
    rank = 3
    return 3
  elif p4 == "":
    p4 = lane
    rank = 4
    return 4
  else:
    print("That is too many cars.  Reset the race:")
  
def getTime(lane):
  timer = (datetime.now() - dt_RaceStart)
  timer = float(str(timer.seconds) + "." + str(timer.microseconds / 1000))
  return timer
  
def outResetDisp():
  for i in range(0, 4, 1):
    dispTimeL1.set_digit_raw(i, 0x40)
  dispTimeL1.write_display()
  for i in range(0, 4, 1):
    dispTimeL2.set_digit_raw(i, 0x40)
  dispTimeL2.write_display()
  #~ for i in range(0, 4, 1):
    #~ dispTimeL3.set_digit_raw(i, 0x40)
  #~ dispTimeL3.write_display()
  #~ for i in range(0, 4, 1):
    #~ dispTimeL4.set_digit_raw(i, 0x40)
  #~ dispTimeL4.write_display()

def outTimeDisp(lane, timer):
  if lane == 1:
    dispTimeL1.clear()
    dispTimeL1.print_float(timer)
    dispTimeL1.write_display()
  elif lane == 2:
    dispTimeL2.clear()
    dispTimeL2.print_float(timer)
    dispTimeL2.write_display()
  #~ elif lane == 3:
    #~ dispTimeL3.clear()
    #~ dispTimeL3.print_float(timer)
    #~ dispTimeL3.write_display()
  #~ elif lane == 4:
    #~ dispTimeL4.clear()
    #~ dispTimeL4.print_float(timer)
    #~ dispTimeL4.write_display()
  else:
    print("No Display for that lane " + str(lane))
  
GPIO.add_event_detect(22, GPIO.RISING, callback=raceStart, bouncetime=10000)
GPIO.add_event_detect(23, GPIO.RISING, callback=lane1, bouncetime=3000)
GPIO.add_event_detect(24, GPIO.RISING, callback=lane2, bouncetime=3000)
GPIO.add_event_detect(25, GPIO.RISING, callback=lane3, bouncetime=3000)
GPIO.add_event_detect(4, GPIO.RISING, callback=lane4, bouncetime=3000)
GPIO.add_event_detect(27, GPIO.RISING, callback=raceStart, bouncetime=3000)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
while True:
    time.sleep(.001)
