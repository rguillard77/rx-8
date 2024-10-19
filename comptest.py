#!/usr/bin/env python
#https://learn.adafruit.com/adafruit-4-channel-adc-breakouts/python-circuitpython
import board
import busio
import time
import sys
import requests
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode

duration = 10.0

ads = ADS.ADS1115(i2c)
ads.mode = Mode.CONTINUOUS
chan = AnalogIn(ads, ADS.P0)

print("Crank to begin")
try:
  while chan.value < 4200.0:
    pass
except:
  sys.exit(0)

now = time.time()
deadline = now + duration
records = []

while now < deadline:
  now = time.time()
  r = "%f;%d" % (now, chan.value)
  print(r)
  records.append(r)
  time.sleep(0.01)

action = input("Send ? (F)ront/(R)ear/(C)ancel: ")

if action.lower() == "f":
  action = "FRONT"
elif action.lower() == "r":
  action = "REAR"
else:
  sys.exit(0)

url = f"http://nddl.guillard.info:9101/report/{action}"
x = requests.post(url, data = "\n".join(records))
print(x.status_code)
