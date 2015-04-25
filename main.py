#!/usr/bin/env python2

#  Call all of the imports
print("hello")
with open("/home/pi/test.txt", "a") as myfile:
  myfile.write("Something to append")
