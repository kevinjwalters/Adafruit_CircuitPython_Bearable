# bearable-scanner v1.0
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
import digitalio
import bearable

board_led = digitalio.DigitalInOut(board.D13)
board_led.direction = digitalio.Direction.OUTPUT

sclpin = board.D2
sdapin = board.D0
# Bus speed can be increased for slightly faster updates
# tested at 500kHz at ~40cm
i2c = busio.I2C(sclpin, sdapin, frequency = 100*1000)

# default is auto_write=True
bear = bearable.Bearable(i2c)

# approx positions of leds in mm
# pylint: disable=bad-whitespace
xpos = [  0,  9,  16, 18, 16,  9,  0, -9, -16, -18, -16,  -9]
ypos = [-12, -12, -8,  0,  8, 12, 12, 12,   8,   0,  -8, -12]
# pylint: enable=bad-whitespace

currentpos = 0
incr = 1
currentincr = incr
limit = max(xpos) // incr * incr
numleds = len(bear)

# vary the width, small variations work best
lowerwidth = 0.5
currentwidth = 1.0
upperwidth = 4.0
widthincr  = 0.0025
currentwidthincr = widthincr

# make a lookup table for the range, -1 is for no value
# this didn't make any real difference in performance
# plus need support for variable width
#lookup = [-1] * (max(xpos) - min(xpos) + 1)

def setleds(bear, pos, width=1.0):
    newval = [0] * numleds
    for i in range(numleds):
        posdiff = pos - xpos[i]
        if posdiff < 0: posdiff = -posdiff  ### fast abs() ?
        newval[i] = width / (posdiff + width)
    bear[:] = newval
    return newval
    
### timing variables
timeridx = 0
timercount = 20
lasttime = time.monotonic()

while True:
    setleds(bear, currentpos, currentwidth)

    currentpos += currentincr
    # change direction if we have reached either end
    if currentpos < -limit:
        currentpos = -limit + incr
        currentincr = incr
    elif currentpos > limit:
        currentpos = limit - incr
        currentincr = -incr

    # adjust width
    currentwidth += currentwidthincr
    if currentwidth < lowerwidth:
        currentwidth = lowerwidth
        currentwidthincr = widthincr
    elif currentwidth > upperwidth:
        currentwidth = upperwidth
        currentwidthincr = -widthincr

    # takes 15ms on a Gemma M0 with 100kHz i2c, 500kHz 13ms
    timeridx += 1
    if timeridx >= timercount:
        now = time.monotonic()
        print("time per loop is {:f}.format ms".format((now - lasttime) / timercount * 1000.0))
        timeridx = 0
        lasttime = now
        
    # time.sleep(0.05) 
    board_led.value = not board_led.value
