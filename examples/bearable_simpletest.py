# bearable_simpletest v1.0
# 
# tested with CircuitPython 2.2.0 on GEMMA M0 with 2.2k pull-up resistors

# copy this file to Gemma M0 as main.py 
# needs lib/adafruit_bus_device/i2c_device.mpy and lib/bearable.py

# MIT License

# Copyright (c) 2018 Kevin J. Walters

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import board
import busio
import time
import bearable

sclpin = board.D2
sdapin = board.D0
i2c = busio.I2C(sclpin, sdapin, frequency = 100*1000)
ledcount = 12

# default is auto_write=True
bear1 = bearable.Bearable(i2c)

bear1.fill(0.0)
time.sleep(1) 
bear1.fill(0.5)
time.sleep(1) 
bear1.fill(1.0)
time.sleep(1) 
bear1.fill(0.0)
time.sleep(1) 

print('\nread_pin')
for i in range(5):
    pinval = bear1.read_pin()
    time.sleep(1)
