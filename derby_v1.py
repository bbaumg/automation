
#!/usr/bin/env python3
# script by Alex Eames http://RasPi.tv
# http://RasPi.tv/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3
import RPi.GPIO as GPIO
import sys
import time
from datetime import datetime
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


def gpio_18(channel):
    end_time_18 = (datetime.now() - start_time)
    print "Pin 18 = " + str(end_time_18)

def gpio_23(channel):
    end_time_23 = (datetime.now() - start_time)
    print "Pin 23 = " + str(end_time_23)

def gpio_24(channel):
    end_time_24 = (datetime.now() - start_time)
    print "Pin 24 = " + str(end_time_24)

def gpio_25(channel):
    end_time_25 = (datetime.now() - start_time)
    print "Pin 25 = " + str(end_time_25)

def gpio_4(channel):
    end_time_4 = (datetime.now() - start_time)
    print "Pin 4 = " + str(end_time_4)

def gpio_17(channel):
    end_time_17 = (datetime.now() - start_time)
    print "Pin 17 = " + str(end_time_17)

def gpio_14(channel):
    end_time_14 = (datetime.now() - start_time)
    print "Pin 14 = " + str(end_time_14)
    
def gpio_15(channel):
    end_time_15 = (datetime.now() - start_time)
    print "Pin 15 = " + str(end_time_15)

def gpio_8(channel):
    end_time_8 = str((datetime.now() - start_time))
    end_time_8 = end_time_8[::2]
    print "Pin 8 = " + end_time_8

def gpio_7(channel):
    global start_time
    start_time = datetime.now()
    print "Start of race = " + str(start_time)

GPIO.add_event_detect(18, GPIO.FALLING, callback=gpio_18, bouncetime=3000)
GPIO.add_event_detect(23, GPIO.FALLING, callback=gpio_23, bouncetime=3000)
GPIO.add_event_detect(24, GPIO.FALLING, callback=gpio_24, bouncetime=3000)
GPIO.add_event_detect(25, GPIO.FALLING, callback=gpio_25, bouncetime=3000)
GPIO.add_event_detect(4, GPIO.FALLING, callback=gpio_4, bouncetime=3000)
GPIO.add_event_detect(17, GPIO.FALLING, callback=gpio_17, bouncetime=3000)
GPIO.add_event_detect(14, GPIO.FALLING, callback=gpio_14, bouncetime=3000)
GPIO.add_event_detect(15, GPIO.FALLING, callback=gpio_15, bouncetime=3000)
GPIO.add_event_detect(8, GPIO.FALLING, callback=gpio_8, bouncetime=3000)
GPIO.add_event_detect(7, GPIO.FALLING, callback=gpio_7, bouncetime=10000)

try:
    print "Waiting for rising edge on port 22"
    GPIO.wait_for_edge(22, GPIO.FALLING)
    print "Rising edge detected on port 22. Here endeth the third lesson."

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit

