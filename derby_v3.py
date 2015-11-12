#!/usr/bin/env python3
import RPi.GPIO as GPIO
import sys
import time
import math
import signal
import logging
from datetime import datetime
from Adafruit_LED_Backpack import SevenSegment

# Setup logging
logging.basicConfig(
  level='CRITICAL', 
  format='%(asctime)s - %(levelno)s - %(funcName)s - %(message)s', 
  datefmt = '%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.OUT)

dispTimeL1 = SevenSegment.SevenSegment(address=0x70)
dispTimeL1.begin()
dispTimeL1.colon = False

dispTimeL2 = SevenSegment.SevenSegment(address=0x71)
dispTimeL2.begin()
dispTimeL2.colon = False

val_Lane2Disp = {1:0, 2:1, 3:3, 4:4}

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

def raceStart(channel):
  global dt_RaceStart
  dt_RaceStart = datetime.now()
  print("Start of race = " + str(dt_RaceStart))
  getRank("START")
  outResetDisp()

def lane1(channel):
  lane = 1
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
  
  if lane == "START":
    p1 = ""
    p2 = ""
    p3 = ""
    p4 = ""
    GPIO.output(17, False)
  elif p1 == "":
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
    GPIO.output(17, True)
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

def outTimeDisp_v1(lane):
  timer = (datetime.now() - dt_RaceStart)
  timer = float(str(timer.seconds) + "." + str(timer.microseconds / 1000))
  print(timer)
  if lane == 1:
    dispTimeL1.clear()
    dispTimeL1.print_float(timer)
    dispTimeL1.write_display()
    print("L1 = " + str(timer))
  elif lane == 2:
    print("L2 = " + str(timer))
  elif lane == 3:
    print("L3 = " + str(timer))
  elif lane == 4:
    print("L4 = " + str(time))
  #segment.writeDigit(1, 8)
  
GPIO.add_event_detect(18, GPIO.RISING, callback=raceStart, bouncetime=10000)
GPIO.add_event_detect(23, GPIO.RISING, callback=lane1, bouncetime=3000)
GPIO.add_event_detect(24, GPIO.RISING, callback=lane2, bouncetime=3000)
GPIO.add_event_detect(25, GPIO.RISING, callback=lane3, bouncetime=3000)
GPIO.add_event_detect(4, GPIO.RISING, callback=lane4, bouncetime=3000)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
while True:
    time.sleep(.001)
