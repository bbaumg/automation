#!/usr/bin/env python

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
#~ from sets import Set
#~ from collections import deque
from datetime import datetime
from Adafruit_LED_Backpack import SevenSegment
from neopixel import *

# Setup logging
logging.basicConfig(
  level='ERROR', 
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

#~ try:
  #~ # Indicator LED Configuration:  Addressable Pixels
  #~ cstLEDCount   = 4       # Number of LED pixels.
  #~ cstLEDPin     = 18      # GPIO pin connected to the pixels (must support PWM!).
  #~ cstLEDFreqHZ  = 800000  # LED signal frequency in hertz (usually 800khz)
  #~ cstLEDDMA     = 5       # DMA channel to use for generating signal (try 5)
  #~ cstLEDInvert  = False   # True to invert the signal (when using NPN transistor level shift)
  #~ strip = Adafruit_NeoPixel(cstLEDCount, cstLEDPin, cstLEDFreqHZ, cstLEDDMA, cstLEDInvert)
  #~ strip.begin()
#~ except:
  #~ print("I guess it failed")

#~ dispTimeL1 = SevenSegment.SevenSegment(address=0x70)
#~ dispTimeL1.begin()
#~ dispTimeL1.colon = False

#~ dispTimeL2 = SevenSegment.SevenSegment(address=0x71)
#~ dispTimeL2.begin()
#~ dispTimeL2.colon = False

#~ dispTimeL3 = SevenSegment.SevenSegment(address=0x72)
#~ dispTimeL3.begin()
#~ dispTimeL3.colon = False

#~ dispTimeL4 = SevenSegment.SevenSegment(address=0x73)
#~ dispTimeL4.begin()
#~ dispTimeL4.colon = False

dictDisplays = {1:0x70, 2:0x71, 3:0x72, 4:0x73}
#dictDisplays = {1:0x70, 2:0x71}
listValues = {1:0x01, 2:0x02, 3:0x04, 4:0x08, 5:0x10, 6:0x20, 7:0x3f,
              8:0x00, 9:0x3f, 10:0x00, 11:0x3f, 12:0x00, 13:0x3f}
for x in listValues:
  for i in dictDisplays:
    try:
      objDisp_i = SevenSegment.SevenSegment(address=dictDisplays[i])
      objDisp_i.begin()
      for ii in range(0,4,1):
        objDisp_i.set_digit_raw(ii, listValues[x])
      objDisp_i.write_display()
    except IOError as e:
      logger.error("The display caused an error for lane " + str(i))
    except:
      logger.exception("An unknown error happened" + str(sys.exc_info()[0]))
  time.sleep(.01)
  
  
# Disctionary list to hold key value pair of lane to dispaly...
flipflop = False
dictPin2Lane = {23:1, 24:2, 25:3, 4:4}
dictLaneTime = {1:0, 2:0, 3:0, 4:0}
dictLanePlace = {1:0, 2:0, 3:0, 4:0}
listPlacement = []

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def raceStart(channel):
  global dt_RaceStart
  dt_RaceStart = datetime.now()
  print("Start of race = " + str(dt_RaceStart))
  dictPin2Lane = {23:1, 24:2, 25:3, 4:4}
  dictLaneTime = {1:0, 2:0, 3:0, 4:0}
  dictLanePlace = {1:0, 2:0, 3:0, 4:0}
  del listPlacement[:]
  outResetDisp()

def lane_v2(channel):
  lane = dictPin2Lane[channel]
  if listPlacement.count(lane) == 0:
    listPlacement.append(lane)
    timer = (datetime.now() - dt_RaceStart)
    timer = float(str(timer.seconds) + "." + str(timer.microseconds / 1000))
    dictLaneTime[lane] = timer
    outTimeDisp(lane)
    dictLanePlace[lane] = listPlacement.index(lane)+1
  else:
    print("That car has already placed, it can't place again")

def processRace(lane):
  global l1
  global l2
  global l3
  global l4
  #~ print("Lane " + str(lane) + " = ")
  finishTime = getTime(lane)
  finishRank = getRank(lane)
  #~ print(finishTime)
  #~ print(finishRank)
  outTimeDisp(lane, finishTime)
  if lane == 1:
    l1 = True
  elif lane == 2:
    l2 = True
  elif lane == 3:
    l3 = True
  elif lane == 4:
    l4 = True
  else:
    print("That lane does not exist")

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
  for i in dictDisplays:
    try:
      objDisp_i = SevenSegment.SevenSegment(address=dictDisplays[i])
      objDisp_i.begin()
      for ii in range(0,4,1):
        objDisp_i.set_digit_raw(ii, 0x40)
      objDisp_i.write_display()
    except IOError as e:
      logger.error("The display caused an error for lane " + str(i))
    except:
      print("There was an error writing to display " + str(lane))
      logger.exception(str(sys.exc_info()[0]))

def outTimeDisp(lane):
  global dictDisplays
  global dictLaneTime
  print("outTimeDisp" + str(lane))
  i = lane
  try:
    objDisp_i = SevenSegment.SevenSegment(address=dictDisplays[i])
    objDisp_i.begin()
    objDisp_i.print_float(dictLaneTime[i])
    objDisp_i.write_display()
  except IOError as e:
    logger.error("The display caused an error for lane " + str(i))
  except:
    print("There was an error writing to display " + str(lane))
    logger.exception(str(sys.exc_info()[0]))
    
def outRankDisp(lane):
  global dictDisplays
  global dictLanePlace
  print("outRankDisp" + str(lane))
  i = lane
  try:
    objDisp_i = SevenSegment.SevenSegment(address=dictDisplays[i])
    objDisp_i.begin()
    objDisp_i.print_number_str(str(dictLanePlace[i])+ " ")
    objDisp_i.write_display()
  except IOError as e:
    logger.error("The display caused an error for lane " + str(i))
  except:
    print("There was an error writing to display " + str(lane))
    logger.exception(str(sys.exc_info()[0]))


GPIO.add_event_detect(22, GPIO.RISING, callback=raceStart, bouncetime=10000)
GPIO.add_event_detect(23, GPIO.RISING, callback=lane_v2, bouncetime=3000)
GPIO.add_event_detect(24, GPIO.RISING, callback=lane_v2, bouncetime=3000)
GPIO.add_event_detect(25, GPIO.RISING, callback=lane_v2, bouncetime=3000)
GPIO.add_event_detect(4, GPIO.RISING, callback=lane_v2, bouncetime=3000)
GPIO.add_event_detect(27, GPIO.RISING, callback=raceStart, bouncetime=3000)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
while True:
  if len(listPlacement) != 0:
    if flipflop == True:
      for lane in dictLaneTime:
        outTimeDisp(lane)
      flipflop = False
    else:
      #~ for lane in dictLanePlace:
        #~ outRankDisp(lane)
      #~ for i in dictDisplays:
        #~ objDisp_i = SevenSegment.SevenSegment(address=dictDisplays[i])
        #~ objDisp_i.begin()
        #~ print(dictLanePlace[i])
        #~ objDisp_i.print_number_str(str(dictLanePlace[i])+ " ")
        #~ objDisp_i.write_display()
      #~ print(str(len(listPlacement)) + " = " + str(listPlacement))
      flipflop = True
  time.sleep(2)
