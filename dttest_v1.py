#!/usr/bin/env python3
import RPi.GPIO as GPIO
import sys
import time
import math
import random
from datetime import datetime
from datetime import timedelta
from Adafruit_LED_Backpack import SevenSegment

while True:
  dt_RaceStart = datetime.now()
  random.seed(datetime.now())
  time.sleep(float(random.randint(800,3000))/1000)
  timer = (datetime.now() - dt_RaceStart)
  print timer
  print timer.seconds
  print timer.microseconds / 10000
  print str(timer.seconds) + "." + str(timer.microseconds / 10000)
  print float(str(timer.seconds) + "." + str(timer.microseconds / 10000))
  timer = float(str(timer.seconds) + "." + str(timer.microseconds / 10000))

  display = SevenSegment.SevenSegment(address=0x71)
  display.begin()
  display.set_colon(False)
  display.print_float(timer)
  display.write_display()

  time.sleep(float(random.randint(10,100))/1000)
  timer = (datetime.now() - dt_RaceStart)
  print timer
  print timer.seconds
  print timer.microseconds / 10000
  print str(timer.seconds) + "." + str(timer.microseconds / 10000)
  print float(str(timer.seconds) + "." + str(timer.microseconds / 10000))
  timer = float(str(timer.seconds) + "." + str(timer.microseconds / 10000))

  display = SevenSegment.SevenSegment(address=0x70)
  display.begin()
  display.set_colon(False)
  display.print_float(timer)
  display.write_display()
  
  time.sleep(1)
  
  display = SevenSegment.SevenSegment(address=0x70)
  display.begin()
  display.set_colon(False)
  for i in range(0, 4, 1):
    display.set_digit_raw(i, 0x40)
  display.write_display()
  
  time.sleep(1)
