import ephem
import datetime

#now = datetime.datetime.now()
now = datetime.datetime.strptime("2015-04-26 22:30:55", "%Y-%m-%d %H:%M:%S")
moon = ephem.Moon()
sun = ephem.Sun()

local=ephem.Observer()
local.lat='39.12'
local.lon='-94.6'
local.elevation=231
local.date=now
#local.date="2015-04-24 20:00:55"
local.horizon='0:34'

nextSet = ephem.localtime(local.next_setting(sun))
nextRise = ephem.localtime(local.next_rising(sun))
prevSet = ephem.localtime(local.previous_setting(sun))
prevRise = ephem.localtime(local.previous_rising(sun))

print("Previous sunrise in KC was: ",ephem.localtime(local.previous_rising(sun)))
print("Previous sunset in KC was: ",ephem.localtime(local.previous_setting(sun)))
print("Next sunrise in KC will be: ",ephem.localtime(local.next_rising(sun)))
print("Next sunset in KC will be: ",ephem.localtime(local.next_setting(sun)))
print("Next Full Moon will be: " ,ephem.localtime(ephem.next_full_moon(now)))
print("Next New Moon will be: " ,ephem.localtime(ephem.next_new_moon(now)))
print("Next Solstice will be: " ,ephem.localtime(ephem.next_solstice(now)))
print("Next Equinox will be: " ,ephem.localtime(ephem.next_equinox(now)))
print("Sunrise:" ,local.next_rising(ephem.Sun()).datetime())
print("Sunset:" ,local.next_setting(ephem.Sun()).datetime())
next_sunrise_datetime = local.next_rising(ephem.Sun()).datetime()
next_sunset_datetime = local.next_setting(ephem.Sun()).datetime()

# If it is daytime, we will see a sunset sooner than a sunrise.
it_is_day = next_sunset_datetime < next_sunrise_datetime
print("It's day." if it_is_day else "It's night.")

# If it is nighttime, we will see a sunrise sooner than a sunset.
it_is_night = next_sunrise_datetime < next_sunset_datetime
print("It's night." if it_is_night else "It's day.")

if nextSet < nextRise:
	print("Day Time")

if nextRise < nextSet:
	print("Night Time")
