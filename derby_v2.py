#!/usr/bin/env python3
import RPi.GPIO as GPIO
import sys
import time
import signal
from datetime import datetime
from Adafruit_7Segment import SevenSegment

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

segment = SevenSegment(address=0x70)
segment.setColon(0)
#segment.print_hex(0, '0x40')

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)

def raceStart(channel):
  global dt_RaceStart
  dt_RaceStart = datetime.now()
  #print "Start of race = " + str(dt_RaceStart)
  carFinished("START")

def lane1(channel):
  lane = 1
  carFinished(lane)

def lane2(channel):
  lane = 2
  carFinished(lane)

def lane3(channel):
  lane = 3
  carFinished(lane)

def lane4(channel):
  lane = 4
  carFinished(lane)

def lane5(channel):
  lane = 5
  carFinished(lane)

def lane6(channel):
  lane = 6
  carFinished(lane)

def carFinished(lane):
  global p1
  global p2
  global p3
  global p4
  global p5
  global p6
  dt_laneEnd = str((datetime.now() - dt_RaceStart))[5:12]

  if lane == "START":
    p1 = ""
    p2 = ""
    p3 = ""
    p4 = ""
    p5 = ""
    p6 = ""
    print("Let the Race Begin!!!")
    segment.writeDigitRaw(0, 0x40)
    segment.writeDigitRaw(1, 0x40)
    segment.writeDigitRaw(3, 0x40)
    segment.writeDigitRaw(4, 0x40)
  elif p1 == "":
    p1 = lane
    segment.writeDigit(lane-1, 1)
    place = "1st Place"
  elif p2 == "":
    p2 = lane
    segment.writeDigit(lane-1, 2)
    place = "2nd Place"
  elif p3 == "":
    p3 = lane
    segment.writeDigit(lane-2, 3)
    place = "3rd Place"
  elif p4 == "":
    p4 = lane
    segment.writeDigit(lane-2, 4)
    place = "4th Place"
  elif p5 == "":
    p5 = lane
    place = "5th Place"
  elif p6 == "":
    p6 = lane
    place = "6th Place"
  if lane != "START":
    print("Lane " + str(lane) + " you finished " + place + "(" + dt_laneEnd + ")")
    if lane == 1:
    elif lane ==2:
    elif lane ==3:
    elif lane ==4:

def get_rank(lane):
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
    segment.writeDigit(lane-1, 1)
    place = "1st Place"
  elif p2 == "":
    p2 = lane
    segment.writeDigit(lane-1, 2)
    place = "2nd Place"
  elif p3 == "":
    p3 = lane
    segment.writeDigit(lane-2, 3)
    place = "3rd Place"
  elif p4 == "":
    p4 = lane
    segment.writeDigit(lane-2, 4)
    place = "4th Place"
  elif p5 == "":
    p5 = lane
    place = "5th Place"
  elif p6 == "":
    p6 = lane
    place = "6th Place"


def get_time(lane):



GPIO.add_event_detect(18, GPIO.FALLING, callback=raceStart, bouncetime=10000)
GPIO.add_event_detect(23, GPIO.FALLING, callback=lane1, bouncetime=3000)
GPIO.add_event_detect(24, GPIO.FALLING, callback=lane2, bouncetime=3000)
GPIO.add_event_detect(25, GPIO.FALLING, callback=lane3, bouncetime=3000)
GPIO.add_event_detect(4, GPIO.FALLING, callback=lane4, bouncetime=3000)
GPIO.add_event_detect(17, GPIO.FALLING, callback=lane5, bouncetime=3000)
GPIO.add_event_detect(22, GPIO.FALLING, callback=lane6, bouncetime=3000)


signal.signal(signal.SIGINT, signal_handler)
print 'Press Ctrl+C'
while True:
    time.sleep(.01)

