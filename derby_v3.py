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
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

dispMain = SevenSegment.SevenSegment(address=0x70)
dispMain.begin()
dispMain.colon = False

dispTimeL1 = SevenSegment.SevenSegment(address=0x71)
dispTimeL1.begin()
dispTimeL1.colon = False

val_Lane2Disp = {1:0, 2:1, 3:3, 4:4}

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)

def raceStart(channel):
  global dt_RaceStart
  dt_RaceStart = datetime.now()
  print "Start of race = " + str(dt_RaceStart)
  getRank("START")

def lane1(channel):
  lane = 1
  getRank(lane)

def lane2(channel):
  lane = 2
  getRank(lane)

def lane3(channel):
  lane = 3
  getRank(lane)

def lane4(channel):
  lane = 4
  getRank(lane)

def lane5(channel):
  lane = 5
  getRank(lane)

def lane6(channel):
  lane = 6
  getRank(lane)

def getRank(lane):
  global p1
  global p2
  global p3
  global p4
  global p5
  global p6

  if lane == "START":
    p1 = ""
    p2 = ""
    p3 = ""
    p4 = ""
    p5 = ""
    p6 = ""  
  elif p1 == "":
    p1 = lane
    rank = 1
    #place = "1st Place"
  elif p2 == "":
    p2 = lane
    rank = 2
    #place = "2nd Place"
  elif p3 == "":
    p3 = lane
    rank = 3
    #place = "3rd Place"
  elif p4 == "":
    p4 = lane
    rank = 4
    #place = "4th Place"
  elif p5 == "":
    p5 = lane
    rank = 5
    #place = "5th Place"
  elif p6 == "":
    p6 = lane
    rank = 6
    #place = "6th Place"
  else:
    print("Too many winnders")
  
  if lane == "START":
    outResetDisp()
  else:
    dispMain.set_digit(lane-1, rank)
    dispMain.write_display()
    outTimeDisp(lane)
    print("Car in lane " + str(lane) + " Ranked " + str(rank))


  
def getTime(lane):
  dt_laneEnd = str((datetime.now() - dt_RaceStart))[5:12]

def outResetDisp():
  for i in range(0, 4, 1):
    dispMain.set_digit_raw(i, 0x40)
  dispMain.write_display()
  for i in range(0, 4, 1):
    dispTimeL1.set_digit_raw(i, 0x40)
  dispTimeL1.write_display()

def outTimeDisp(lane):
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
GPIO.add_event_detect(23, GPIO.RISING, callback=lane1, bouncetime=1)
GPIO.add_event_detect(24, GPIO.RISING, callback=lane2, bouncetime=1)
GPIO.add_event_detect(25, GPIO.RISING, callback=lane3, bouncetime=1)
GPIO.add_event_detect(4, GPIO.RISING, callback=lane4, bouncetime=1)
GPIO.add_event_detect(17, GPIO.RISING, callback=lane5, bouncetime=1)
GPIO.add_event_detect(22, GPIO.RISING, callback=lane6, bouncetime=1)


signal.signal(signal.SIGINT, signal_handler)
print 'Press Ctrl+C'
while True:
    time.sleep(.001)
