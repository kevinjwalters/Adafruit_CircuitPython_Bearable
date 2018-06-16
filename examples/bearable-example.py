# bearable-example v1.0
# 
# tested with CircuitPython 2.2.0 on GEMMA M0 with 2.2k pull-up resistors

# copy this file to Gemma M0 as main.py 
# needs lib/adafruit_bus_device/i2c_device.mpy and lib/adafruit_bearable.py

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
import digitalio
import adafruit_bearable

board_led = digitalio.DigitalInOut(board.D13)
board_led.direction = digitalio.Direction.OUTPUT

sclpin = board.D2
sdapin = board.D0
i2c = busio.I2C(sclpin, sdapin, frequency = 100*1000)

# default is auto_write=True
bear = adafruit_bearable.Bearable(i2c)

intbrightness = 8  # 8 is max hardware integer value
incr = -1

while True:
    brightness = intbrightness / 8.0
    print('setting brightness to {:f} ({:d})'.format(brightness, intbrightness))
    bear.fill(brightness)
    intbrightness += incr
    if intbrightness < 0:
        intbrightness = 1
        incr = 1
    elif intbrightness > 8:
        intbrightness = 7
        incr = -1
    pinval = bear.read_pin()
    print('read_pin return {:d}'.format(pinval))

    time.sleep(0.1) 
    board_led.value = not board_led.value
