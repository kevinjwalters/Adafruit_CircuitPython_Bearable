# Pimoroni Bearable(s) library for CircuitPython

# The MIT License (MIT)

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
"""
`Bearable`
====================================================

Driver for the Pimoroni Bearable(s) bear and fox badges using i2c pads.

* Author(s): Kevin J. Walters

Implementation Notes
--------------------

Inspired by Pimoroni and:

 * Phil Underwood hacking the Bareables Badge: https://lorrainbow.wordpress.com/2017/11/18/guest-blogger-phil-underwood-hacking-the-bareables-badge/
 * Raspberry Pi bearables library: https://github.com/sandyjmacdonald/bearables

**Hardware:**
 * Pimoroni Bearables Bear kit: https://shop.pimoroni.com/products/bearables-bear-kit 
 * Pimoroni Bearables Fox kit: https://shop.pimoroni.com/products/bearables-fox-kit

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

 * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""

# imports
import time
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/kevinjwalters/CircuitPython_Bearable.git"


# i2c commands extracted from
# https://github.com/sandyjmacdonald/bearables/blob/master/library/bearables/__init__.py

# pylint: disable=bad-whitespace
_BEAR_SET_MODE         = const(0x00)
_BEAR_LED_PATTERN_MODE = const(0x10)
_BEAR_LED_DIRECT_MODE  = const(0x11)

_BEAR_SET_LEDS         = const(0x01)

_BEAR_GET_ANALOGUE1    = const(0x07)
_BEAR_SET_PATTERN      = const(0x08)
# pylint: enable=bad-whitespace


class Bearable:
    """
    Driver for the Pimoroni Bearable(s) bear and fox badges using i2c pads.

    Throws exceptions for any i2c errors after retries.
    
    :param ~busio.I2C i2c: the busio.I2C object.
    :param int n: The number of leds on the badge, defaults to 12.
    :param int address: The i2c address of the badge, defaults to 0x15.
    :param float brightness: Global brightness of the pixels between 0.0 and 1.0, defaults to 1.0.
    :param bool auto_write: True if the dotstars should immediately change when
        set. If False, `show` must be called explicitly. Defaults to True.
    :param int retries: The number of retries for i2c communication errors, defaults to 3.
    :param float retrypause: The pause between any retries in seconds, defaults to 0.001 (1ms).
    """

    def __init__(self, i2c, *, n=12, address=0x15, brightness=1.0, auto_write=True, retries=3, retrypause=0.001):
        if brightness < 0.0 or brightness > 1.0:
            raise ValueError("brightness out of range")

        self._i2c = i2c
        self._n = n # 12 LEDs on bear and fox badges
        self._address = address
        self._brightness = brightness
        self._auto_write = auto_write
        self._attempts = retries + 1
        self._retrypause = retrypause

        self._device = I2CDevice(i2c, address)
        # red LED bellow chin is index 0 and order is counter-clockwise
        self._leds = [0.0] * self._n
        # empirical testing suggests this is 8
        # see https://github.com/sandyjmacdonald/bearables/issues/1
        self._maxbrightness = 8
        self._convertfactor = self._maxbrightness * self._brightness
        self._mode = None
        self._pattern = None

    def _set_mode(self, mode):
        """Sends an i2c command to set the badge's mode if that mode has not already been set.
        
        :param int mode: either _BEAR_LED_DIRECT_MODE or _BEAR_LED_PATTERN_MODE.
        """
        if mode == self._mode:
            return

        cmd = bytes([_BEAR_SET_MODE, mode])
        self._i2cwrite(cmd)
        self._mode = mode

    def __setitem__(self, index, val):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._n)
            length = stop - start
            if step != 0:
                length = (length + step - 1) // step
            if len(val) != length:
                raise ValueError("Slice and input sequence size do not match")
            for val_i, in_i in enumerate(range(start, stop, step)):
                self._set_item(in_i, val[val_i])
        else:
            self._set_item(index, val)
        if self._auto_write:
            self.show()
            
    def __getitem__(self, index):
        """Returns the set value between 0.0 and 1.0, not the quantized value."""
        return self._leds[index]
            
    def __len__(self):
        return self._n
                    
    def _set_item(self, index, value):
        self._leds[index] = value
 
    def fill(self, value):
        """
        Set all the pixels to same value:
        
        :param float value: brightness between 0.0 and 1.0.
        """
        for i in range(self._n):
            self._leds[i] = value
        if self._auto_write:
            self.show()
        
    def read_pin(self):
        """Read the value of the analogue input pin.
        
            Return value is an int between 0 and 255.
            Acorn badge is 0 when lying flat and around 45 when vertical.
            A finger pressed across contacts firmly is 1.
            A 2k2 resistor is 208, a 4k4 resistor is 177.
            YMMV.
        """
        self._set_mode(_BEAR_LED_DIRECT_MODE)

        errors = 0
        cmd = bytes([_BEAR_GET_ANALOGUE1])
        buf = bytearray(1)
        for attempt in range(self._attempts):
            try:
                with self._device:
                    self._device.write(cmd)
                    self._device.readinto(buf)
            except Exception as e:
                errors += 1
                if errors == self._attempts:
                    raise RuntimeError("i2c last exception after retries: " + repr(e))
                else:
                    time.sleep(self._retrypause)
        return buf[0]

    def maxbrightness(self):
        """Returns the number of brightness levels the hardware supports (ignoring all off)."""
        return self._maxbrightness
        
    def _pack_leds(self):
        return [(int(self._leds[i] * self._convertfactor) & 0b1111) << 4
                | (int(self._leds[i + 1] * self._convertfactor) & 0b1111) for i in range(0, self._n, 2)]

    def show(self):
        """Displays any set pixels.
        """
        self._set_mode(_BEAR_LED_DIRECT_MODE)
        
        cmd = bytes([_BEAR_SET_LEDS] + self._pack_leds())
        # print('bear in the woods')
        # print(' '.join([hex(i) for i in cmd]))
        self._i2cwrite(cmd)

    def pattern(self, pattern):
        """Puts bear into pattern mode and sets the pattern (0-11).
        """
        self._set_mode(_BEAR_LED_PATTERN_MODE)
        
        cmd = bytes([_BEAR_SET_PATTERN, pattern])
        # print('bear likes a pattern {:d}'.format(pattern))
        # print(' '.join([hex(i) for i in cmd]))
        self._i2cwrite(cmd)
        self._pattern = pattern

    def _i2cwrite(self, data, *, attempts=None):
        errors = 0
        if attempts is None: attempts = self._attempts
        for attempt in range(attempts):
            try:
                with self._device:
                    self._device.write(data)
            except Exception as e:
                errors += 1
                if errors == self._attempts:
                    raise RuntimeError("i2c last exception after retries: " + repr(e))
                else:
                    time.sleep(self._retrypause)

    def _i2cwriteread(self, wdata, rdata, *, attempts=None):
        """Send a command down i2c bus and immediately read reply.

        :param bytes wdata: data to write.
        :param bytearray rdata: size must match reply size.
        """
        errors = 0
        if attempts is None: attempts = self._attempts
        for attempt in range(attempts):
            try:
                with self._device:
                    self._device.write(wdata)
                    self._device.readinto(rdata)
            except Exception as e:
                errors += 1
                if errors == self._attempts:
                    raise RuntimeError("i2c last exception after retries: " + repr(e))
                else:
                    time.sleep(self._retrypause)

