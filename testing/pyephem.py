import ephem
import datetime

now = datetime.datetime.now() #get current time
moon = ephem.Moon()
sun = ephem.Sun()

local=ephem.Observer()
local.lat='39.12'
local.lon='-94.6'
local.elevation=231
local.date=now
local.horizon='0:34'

print("Next sunrise in KC will be: ",ephem.localtime(local.next_rising(sun)))
print("Next sunset in KC will be: ",ephem.localtime(local.next_setting(sun)))
print("Next Full Moon will be: " ,ephem.localtime(ephem.next_full_moon(now)))
print("Next New Moon will be: " ,ephem.localtime(ephem.next_new_moon(now)))
print("Next Solstice will be: " ,ephem.localtime(ephem.next_solstice(now)))
print("Next Equinox will be: " ,ephem.localtime(ephem.next_equinox(now)))
