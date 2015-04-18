#!/usr/bin/env python

#  Call all of the imports
import smbus
import struct
import time
import datetime
import MySQLdb
import os
import logging
from twilio.rest import TwilioRestClient

# Set all of the constants
bus = smbus.SMBus(1)
address = 0x04
cstlogFile = '/var/controller/main.log'
cstDBHost = 'localhost'
cstDBName = 'automation'
cstDBUser = 'automation'
cstDBPass = 'Pass1234'
i2cReadDelay = 2


# Instantiate global variables
varRunAttempts = 0
varRunSuccess = 0
varRunFailure = 0
varRunRetries = 0

# Setup logging
#logLevel = logging.CRITICAL
#logLevel = logging.ERROR
#logLevel = logging.WARNING
#logLevel = logging.INFO
logLevel = logging.DEBUG

#logLevel = DEBUG
logging.basicConfig(
  level=logLevel, 
  format='%(asctime)s - %(levelno)s - %(funcName)s - %(message)s', 
  datefmt = '%Y-%m-%d %H:%M:%S',
  filename = cstlogFile)
logger = logging.getLogger(__name__)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END SETUP - BEGIN FUNCTIONS
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  
# Return the data time as the UNIX epoch
def epochTime():
  value = str(int(time.time())-time.timezone-(time.daylight*3600))
  #value = str(int(time.time())+60*60*(6+int(time.daylight)))
  #value = "T" + str(int(time.mktime(time.localtime())))
  #print time.gmtime()
  #print time.localtime()
  logger.debug(value)
  return value

# Send an SMS message
#   subject = The message to be sent
def sendSMS(subject):
  account_sid = "ACb3a8553d9b1b9cbeab0b045bcec7df4a"
  auth_token  = "c490b1f0318585ecaa786a5422212a1c"
  client = TwilioRestClient(account_sid, auth_token)
   
  message = client.messages.create(body=subject, 
            to="+18162002286", from_="+18163261013")
  print message.sid

# Send a message over i2c to the controller
#   value = The string to send to the controller
def i2cWrite(value):
  logger.debug("Begin Function")
  try:  
    bus.write_byte(address, ord('\1'))
    logger.debug(ord('\1'))
    for character in str(value):
      bus.write_byte(address, ord(character))
      logger.debug(character)
    bus.write_byte(address, ord('\4'))
    logger.debug(ord('\4'))
  except IOError as e:
    logger.error("Comm Error")
  except:
    logger.error("Unexpected error!")
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  logger.debug("End Function")

# Request a byte back from the controller (checksum for i2cWrite)
def i2cRead():
  logger.debug("Begin Function")
  try:
    value = bus.read_byte(address)
    logger.debug("Returned Value = " + str(value))
    return value
  except IOError as e:
    #writeLog(True, "Comm Error")
    logger.debug("Comm Error")
  except:
    logger.error("Unexpected error!")
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  finally:
    logger.debug("End Function")

# Message to device to initiate a time sync.
def devSyncTime():
  logger.info("Begin Function")
  while True:
    number = int(epochTime())
    array = [(number>>(8*i))&0xff for i in range(3,-1,-1)]
    i2cWrite(chr(255)+"T"+chr(array[0])+chr(array[1])+chr(array[2])+chr(array[3]))
    time.sleep(i2cReadDelay)
    result = i2cRead()
    if result == 240:
      logger.info("Successful")
      break
    else:
      logger.warning("Failed to execute (must succeed), will retry...")
  logger.info("End Function")

# Message to device to initiate a time sync.
def devSyncTime_v1():
  logger.info("Begin Function")
  while True:
    i2cWrite("T" + epochTime())
    time.sleep(1)
    result = i2cRead()
    if result == 6:
      logger.info("Successful")
      break
    else:
      logger.warning("Failed to execute (must succeed), will retry...")
  logger.info("End Function")

# Request the sensor reading from the controller for a given sensor
#   sensDevice = Device # of the sensor (reference DB)
#   sensType = # of the sensor type (reference DB)
def devReadSensors_notUsed(sensDevice, sensType):
  logger.info("Begin Function")
  count = 0
  attempts = 3
  logger.debug("Sensor # = " + str(sensType))
  while (count < attempts):
    i2cWrite(chr(sensDevice) + "S" + chr(sensType))
    time.sleep(i2cReadDelay)
    result = i2cRead()
    if result != 241 and result != 242 and result != 255:
      logger.info("Read Sensor " + str(sensDevice) + str(sensType) + \
                  " = " + `result`)
      logger.info("Exit Function")
      return result
    else:
      count = count + 1
      logger.warning("Read Sensor " + str(sensDevice) + str(sensType) + \
                     " = Invalid, will retry.. " \
                     "(" + str(count) + " of " + str(attempts) + ")")
      #time.sleep(1)
      if count == attempts:
      	logger.error("Read Sensor " + str(sensDevice) + str(sensType) + " = FAILED")
      	logger.info("Exit Function")
        return 255
  logger.info("End Function")

# DO NOT USE
# Request the sensor reading from the controller for a given sensor
#   sensDevice = Device # of the sensor (reference DB)
#   sensType = # of the sensor type (reference DB)
def devReadSensors_v1(sensDevice, sensType):
  logger.info("Begin Function")
  count = 0
  attempts = 3
  value = str((sensDevice *10) + sensType)
  logger.debug("Sensor # = " + value)
  while (count < attempts):
    if value == str(21):
      logger.debug("Test Sensor Called = Will not read sensor")
      logger.debug("Forcing value = 0")
      return 0
    i2cWrite("S" + value)
    #time.sleep(1)
    result = i2cRead()
    if result != 255:
      logger.info("Read Sensor " + value + " = " + `result`)
      logger.info("Exit Function")
      return result
    else:
      count = count + 1
      logger.warning("Read Sensor " + value + " = Invalid, will retry.. " \
            "(" + str(count) + " of 10)")
      if count == attempts:
      	logger.error("Read Sensor " + value + " = FAILED")
      	logger.info("Exit Function")
        return 255
  logger.info("End Function")

# DO NOT USE
# Log the sensor data to the DB fro a given sensor.
#   sensID = the ID of the sensor (reference DB)
#   value = the measurement to be logged to the DB
def dbLogSensor_v1(sensID, value):
  logger.info("Begin Function")
  db = MySQLdb.connect(host=cstDBHost, db=cstDBName, 
                       user=cstDBUser, passwd=cstDBPass)
  cursor = db.cursor()
  sql = """
        INSERT INTO tbl_readings
        (sensors_ID, readings_datetime, readings_value)
        VALUES (%s, now(), %s)
        """
  logger.debug(sql)
  args = sensID, value
  try:
    cursor.execute(sql, args)
    db.commit()
    logger.info("Writing Sensor Data = Successful")
  except:
    db.rollback()
    logger.error("Writing Sensor Data = Unexpected error!")
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  finally:
    db.close()
    logger.info("End Function")

# Log the sensor data to the DB fro a given sensor.
#   sensID = the ID of the sensor (reference DB)
#   value = the measurement to be logged to the DB
def dbLogSensor(sensID, value):
  logger.info("Begin Function")
  db = MySQLdb.connect(host=cstDBHost, db=cstDBName, 
                       user=cstDBUser, passwd=cstDBPass)
  cursor = db.cursor()
  args = sensID, value
  try:
    results = cursor.callproc('sp_put_readings',(args))
    db.commit()
    logger.debug(results)
  except:
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  finally:
    cursor.close()
    db.close()
    logger.info("End Function")

# Get a list of valid sensors from the database
def dbGetSensors():
  logger.info("Begin Function")
  db = MySQLdb.connect(host=cstDBHost, db=cstDBName, 
                       user=cstDBUser, passwd=cstDBPass)
  cursor = db.cursor()
  sql = """
        select 
            tbl_sensors.ID,
            tbl_sensors.device_ID,
            tbl_sensors.type_ID,
            tbl_devices.device_description,
            tbl_types.type_description,
            tbl_sensors.sensor_min,
            tbl_sensors.sensor_max
        from
            tbl_sensors
                inner join
            tbl_devices ON tbl_sensors.device_ID = tbl_devices.ID
                inner join
            tbl_types ON tbl_sensors.type_ID = tbl_types.ID
        where
            tbl_sensors.sensor_active is true
        """
  logger.debug("SQL Command = " + sql)
  try:
    cursor.execute(sql)
    logger.debug("SQL Count = " + str(cursor.rowcount))
    results = cursor.fetchall()
    logger.debug("SQL Results = " + str(results))
    return results
  except:
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  finally:
    db.close()  
    logger.info("End Function")

# Get the least sensor value for given sensor from the database
#   sensID = the ID of the sensor (reference DB)
def dbGetReadingsAverage(sensID, timeLimit):
  logger.info("Begin Function")
  db = MySQLdb.connect(host=cstDBHost, db=cstDBName, 
                       user=cstDBUser, passwd=cstDBPass)
  cursor = db.cursor()
  sql = """
        SELECT 
            count(readings_value) as count_readings, 
            cast(avg(readings_value) as unsigned int) as avg_readings_value
        FROM
            tbl_readings
        where
            sensors_ID = %s
                and readings_datetime > date_sub(now(), interval %s minute)
        """
  logger.debug(sql)
  args = sensID, timeLimit
  try:
    cursor.execute(sql, args)
    logger.debug("SQL Count = " + str(cursor.rowcount))
    results = cursor.fetchall()
    logger.debug("SQL Results = " + str(results))
    for row in results:
      logger.debug("SQL Results = " + str(row))
      sensTime = row[0]
      sensValue = row[1]
      return row
  except:
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  finally:
    db.close()  
    logger.debug("End Function")

# Collect the list of sensors and try to poll each one from the controller          
def collectSensors():
  logger.info("Begin Function")
  try:
    results = dbGetSensors()
    logger.debug("dbGetSensors() Results = " + str(results))
    for row in results:
      logger.debug("Row Results = " + str(row))
      sensID = row[0]
      sensDevice = row[1]
      sensType = row[2]
      sensDeviceName = row[3]
      sensTypeName = row[4]
      logger.info("Getting Sensor = " \
            "ID:" + str(sensID) + "" \
            " " + sensTypeName + "(" + str(sensType) + ") on" \
            " " + sensDeviceName + "(" + str(sensDevice) + ")")
      #value = devReadSensors(sensDevice, sensType)
      value = devMessage(chr(sensDevice), "S" + chr(sensType))
      logger.debug("Respone Value = " + str(value))
      if value == 255:
        logger.error("Getting Sensor = " \
                    "ID:" + str(sensID) + " Bad reading.  Value will be ignored")
      else:
        logger.debug("Logging value = " + str(value))
        dbLogSensor(sensID, value)
    logger.info("Collecting list of sensors = Complete")
  except:
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  finally:
    logger.info("End Function")

# Validate the temp thresholds are within min and max values
def validateTemp():
  logger.info("Begin Function")
  try:
    sensors = dbGetSensors()
    logger.debug("dbGetSensors() Results = " + str(sensors))
    for sensor in sensors:
      logger.debug("Row Result = " + str(sensor))
      sensID = sensor[0]
      sensDevice = sensor[1]
      sensType = sensor[2]
      sensDeviceName = sensor[3]
      sensTypeName = sensor[4]
      sensMin = sensor[5]
      sensMax = sensor[6]
      readings = dbGetReadingsAverage(sensID, 60)
      logger.debug("dbGetReadingsAverage() for ID: " 
                   + str(sensID) + " Results = " + str(readings))
      readingCount = readings[0]
      readingAvg = readings[1]
      #if readingCount < 
  except:
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  finally:
    logger.info("End Function")


###  Starting down here, new functions with updated logic.
# First one is to update LEDs
# Generic Device messaging function will replace all device messaging


# Update the LED settings on all remote devices
def updateLEDs():
  logger.info("Begin Function")
  try:
    results = dbGetLEDs()
    logger.debug("dbGetLEDs() Results = " + str(results))
    for row in results:
      logger.debug("Row Results = " + str(row))
      rowID = row[0]
      rowDevice = row[1]
      rowPixel = row[2]
      rowRed = row[3]
      rowGreen = row[4]
      rowBlue = row [5]
      result = devMessage(chr(rowDevice), "LI"+chr(rowPixel)+ \
                          chr(rowRed)+chr(rowGreen)+chr(rowBlue))
      logger.debug("LED Update Result = " + str(result))
  except:
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  finally:
    logger.info("End Function")

# Send general messages to the devices & wait for a response code.
#   devID = the ID of the device (reference DB)
def devMessage(device, message):
  logger.info("Begin Function")
  count = 1
  attempts = 3
  global varRunAttempts
  global varRunSuccess
  global varRunFailure
  global varRunRetries
  logger.debug("Device Message = " + str(message))
  varRunAttempts += 1
  try:
    while True:
      i2cWrite(str(device) + str(message))
      time.sleep(i2cReadDelay)
      result = i2cRead()
      if count >= attempts:
        logger.error("Unable to get valid response = FAILED")
        logger.info("Exit Function")
        varRunFailure += 1
        return 255
        break
      elif result == 240:
        logger.info("Result = Success")
        return "Seccuss"
      elif result == 241:
        logger.error("No RF Response - Attempt Made (" \
                     + str(count) + " of " + str(attempts) + ")")
        varRunRetries += 1
        count += 1
      elif result == 242:
        logger.error("No RF ACK - Attempt Made (" \
                     + str(count) + " of " + str(attempts) + ")")
        varRunRetries += 1
        count += 1
      elif result == 255:
        logger.error("Bad Data response - Attempt Made (" \
                     + str(count) + " of " + str(attempts) + ")")
        varRunRetries += 1
        count += 1
      else:
        logger.info("Response = " + str(result))
        logger.info("End Function")
        varRunSuccess += 1
        return result
        break
  except:
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  finally:
    logger.info("End Function")


# Collect a list of all LED settings from the database
def dbGetLEDs():
  logger.info("Begin Function")
  sql = """
        select ID, 
        Device_ID, 
        LEDs_Pixel, 
        LEDs_Red, 
        LEDs_Green, 
        LEDs_Blue
        from
            tbl_LEDs
        WHERE
            LEDs_Active is true
        """
  try:
    db = MySQLdb.connect(host=cstDBHost, db=cstDBName, 
                         user=cstDBUser, passwd=cstDBPass)
    cursor = db.cursor()
    logger.debug("SQL Command = " + sql)
    cursor.execute(sql)
    logger.debug("SQL Count = " + str(cursor.rowcount))
    results = cursor.fetchall()
    logger.debug("SQL Results = " + str(results))
    return results
  except:
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
  finally:
    db.close()  
    logger.info("End Function")

# Test the database is up and running.



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END FUNCTIONS - BEGIN PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

logger.critical("*****************************************************")
logger.critical("*")
logger.critical("* Starting Program")
logger.critical("*")
logger.critical("*****************************************************")
logger.critical("Log Level = " + str(logLevel))

mysqlTest = False
while mysqlTest == False:
  try:
    db = MySQLdb.connect(host=cstDBHost, db=cstDBName, 
                         user=cstDBUser, passwd=cstDBPass)
    db.close()
    mysqlTest = True
  except:
    logger.exception("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    logger.error("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    mysqlTest = False
    time.sleep(5)


# Function Debug section as this will run first
#devSyncTime()
#time.sleep(20)

while True:
  devSyncTime()
  #collectSensors()
  #logger.critical("-----------------------------------")
  #logger.critical("Total = " + str(varRunAttempts) + "/" 
                  #+ str(varRunSuccess + varRunFailure))
  #logger.critical("Error = " + str(varRunFailure))
  #logger.critical("Success = " + str(varRunSuccess))
  #logger.critical("Success Rate = " + str(float(varRunSuccess) / float(varRunAttempts)))
  #logger.critical("Retries = " + str(varRunRetries))
  #logger.critical("-----------------------------------")
  time.sleep(7)

  #collectSensors() # collect all sensors
  #time.sleep(20)
  # number = int(epochTime())
  # #number = int(1000)
  # array = [(number>>(8*i))&0xff for i in range(3,-1,-1)]
  # teststr = chr(2)+"LI"+chr(25)+chr(255)+chr(255)+chr(255)
  # #teststr = chr(10)+"D"+chr(array[0])+chr(array[1])+chr(array[2])+chr(array[3])
  # #teststr = chr(255)+"T"+chr(array[0])+chr(array[1])+chr(array[2])+chr(array[3])
  # #teststr = chr(2)+"S"+chr(2)
  
  # teststr = chr(2)+"S"+chr(2)
  # logger.debug(teststr)
  # i2cWrite(teststr)
  # time.sleep(2)
  # logger.debug(i2cRead())
  
  # teststr = chr(3)+"LI"+chr(25)+chr(255)+chr(255)+chr(255)
  # logger.debug(teststr)
  # i2cWrite(teststr)
  # time.sleep(2)
  # logger.debug(i2cRead())
  
  # teststr = chr(255)+"T"+chr(array[0])+chr(array[1])+chr(array[2])+chr(array[3])
  # logger.debug(teststr)
  # i2cWrite(teststr)
  # time.sleep(2)
  # logger.debug(i2cRead())

logger.debug("** Calling devSyncTime()")
devSyncTime() # Sync up the time
logger.debug("** Calling collectSensors()")
collectSensors() # collect all sensors
logger.debug("** Calling updateLEDs()")
updateLEDs()

logger.info("Beginning main loop")
while True: # The main loop that will never end
  if time.strftime('%S', time.localtime()) == "00":
    logger.debug("** Holding until the next run")
    logger.debug("** Calling devSyncTime()")
    devSyncTime()
    logger.debug("** Calling collectSensors()")
    collectSensors()
    #logger.debug("** Calling updateLEDs()")
    #updateLEDs()
    #logger.debug("** Calling validateTemp()")
    #validateTemp()
    logger.debug("** Holding until the next run")
  time.sleep(.1)

logging.shutdown()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END PROGRAM
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!















