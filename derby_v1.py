#!/usr/bin/env python3
import RPi.GPIO as GPIO
import sys
import time
import inspect
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
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
segment = SevenSegment(address=0x70)

def gpio_18(channel):
  global start_time
  finishOrder("START")
  start_time = datetime.now()
  print "Start of race = " + str(start_time)

def gpio_23(channel):
  lane = 2
  end_time = str((datetime.now() - start_time))[5:12]
  place = finishOrder(lane)
  print place + " = Lane " + lane[-1:] + " (" + end_time + ")"

def gpio_24(channel):
  lane = 3
  end_time = str((datetime.now() - start_time))[5:12]
  place = finishOrder(lane)
  print place + " = Lane " + lane[-1:] + " (" + end_time + ")"

def gpio_25(channel):
  lane = 4
  end_time = str((datetime.now() - start_time))[5:12]
  place = finishOrder(lane)
  print place + " = Lane " + lane[-1:] + " (" + end_time + ")"

def gpio_4(channel):
  lane = 5
  end_time = str((datetime.now() - start_time))[5:12]
  place = finishOrder(lane)
  print place + " = Lane " + lane[-1:] + " (" + end_time + ")"

def gpio_17(channel):
  lane = 6
  end_time = str((datetime.now() - start_time))[5:12]
  place = finishOrder(lane)
  print place + " = Lane " + lane[-1:] + " (" + end_time + ")"

def gpio_14(channel):
  lane = 7
  end_time = str((datetime.now() - start_time))[5:12]
  place = finishOrder(lane)
  print place + " = Lane " + lane[-1:] + " (" + end_time + ")"

def gpio_15(channel):
  lane = 8
  end_time = str((datetime.now() - start_time))[5:12]
  place = finishOrder(lane)
  print place + " = Lane " + lane[-1:] + " (" + end_time + ")"

def gpio_8(channel):
  lane = 9
  end_time = str((datetime.now() - start_time))[5:12]
  place = finishOrder(lane)
  print place + " = Lane " + str(lane) + " (" + end_time + ")"

def finishOrder(lane):
  global p1st
  global p2nd
  global p3rd
  global p4th
  if lane == "START":
    p1st = ""
    p2nd = ""
    p3rd = ""
    p4th = ""
    segment.writeDigit(0, int(lane))
  elif p1st == "":
    p1st = lane
    segment.writeDigit(0, int(lane))
    return "1st Place"
  elif p2nd == "":
    p2nd = lane
    #segment.writeDigit(1, int(lane))
    return "2nd Place"
  elif p3rd == "":
    p3rd = lane
    #segment.writeDigit(3, int(lane))
    return "3rd Place"
  elif p4th == "":
    p4th = lane
    #segment.writeDigit(4, int(lane))
    return "4th Place"
  else:
    return "ERROR - Too Many Lanes"

GPIO.add_event_detect(18, GPIO.FALLING, callback=gpio_18, bouncetime=3000)
GPIO.add_event_detect(23, GPIO.FALLING, callback=gpio_23, bouncetime=3000)
GPIO.add_event_detect(24, GPIO.FALLING, callback=gpio_24, bouncetime=3000)
GPIO.add_event_detect(25, GPIO.FALLING, callback=gpio_25, bouncetime=3000)
GPIO.add_event_detect(4, GPIO.FALLING, callback=gpio_4, bouncetime=3000)
GPIO.add_event_detect(17, GPIO.FALLING, callback=gpio_17, bouncetime=3000)
#GPIO.add_event_detect(14, GPIO.FALLING, callback=gpio_14, bouncetime=3000)
#GPIO.add_event_detect(15, GPIO.FALLING, callback=gpio_15, bouncetime=3000)
#GPIO.add_event_detect(8, GPIO.FALLING, callback=gpio_8, bouncetime=3000)
#GPIO.add_event_detect(7, GPIO.FALLING, callback=gpio_7, bouncetime=10000)

try:
  print "Waiting for rising edge on port 22"
  GPIO.wait_for_edge(22, GPIO.FALLING)
  print "Rising edge detected on port 22. Here endeth the third lesson."

except KeyboardInterrupt:
  GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit

