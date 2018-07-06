
### TODO - i still don't understand how to replace each method in a mocked class with
###        a coded implementation

### Currently executing on linux, e.g.

### $ PYTHONPATH=.. python3 noodling-test1.py
### testModeAlternation (__main__.TestI2cComms) ... ok
### testSequenceAssignmentsAutoshowOn (__main__.TestI2cComms) ... ok
### 
### ----------------------------------------------------------------------
### Ran 2 tests in 0.005s
### 
### OK

import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import call
from unittest.mock import create_autospec

import os
debug = int(os.getenv('BEARDEBUG',0))
verbose = int(os.getenv('BEARVERBOSE',2))

##class PimoroniBearBagdeSimulatorI2CBus:
##    def readinto(self, buf):
##        print("CANNOT BE THIS EASY I")
##        buf[0] = 0x03
##
##    def simulate(buf):
##        print("Hooked into side_effect")


import sys
### Need to learn more about patch to determine optimal
### way to mock I2CDevice in adafruit_bus_device.i2c_device
#### MagicMock needed to deal with __enter__ and __exit__
##sys.modules['adafruit_bus_device.i2c_device.I2CDevice'] = MagicMock(wraps=PimoroniBearBagdeSimulatorI2CDevice)
sys.modules['adafruit_bus_device.i2c_device.I2CDevice'] = MagicMock()
sys.modules['adafruit_bus_device.i2c_device'] = MagicMock()
sys.modules['busio'] = Mock()

### MicroPython/CircuitPython have const(), Python doesn't
### there may be neater way to do this
if hasattr(__builtins__, 'const'):
    pass
else:
    __builtins__.const = lambda x: x

import bearable

import busio
import bearable

### TODO - move this into TestI2cComms ?
# create a mocked busio.I2C(sclpin, sdapin, frequency = 100*1000)
### I can't do this unless I get a real busio library
## mockedi2c = create_autospec(spec=busio.I2C, instance=True)

##class PimoroniBearBagdeSimulatorI2C:
##    def __init__(self, scl, sda, *, frequency=400000):
##        print("INIT")
##
##    def readfrom_into(address, buffer, *, start=None, end=None):
##        print("readfrom_into")
##
##    def writeto(address, buffer, *, start=None, end=None, stop=True):
##        print("writeto")
##
#mockedi2c = create_autospec(spec=PimoroniBearBagdeSimulatorI2C, instance=True)

mockedi2c = Mock()


class TestI2cComms(unittest.TestCase):

    def testSequenceAssignmentsAutoshowOn(self):
        """
        Test 
        1) creation of Bearable instance,
        2) first sequence assignment to the object which will also write a mode selection before the write of data,
        3) assignment over-writing previous value which will write a single update,
        4) third sequence assigment at end of sequence.
        """
        # default is auto_write=True
        badge_i2c_addr = 0x15
        classreached = len(bearable.I2CDevice.mock_calls)
        reached = 0
        bear1 = bearable.Bearable(mockedi2c)
        
        if type(bear1).__name__ != "Bearable":
            print('Bear is not a Bearable!')
        self.assertEqual(bearable.I2CDevice.mock_calls[classreached:],
                         [call(mockedi2c, badge_i2c_addr)
                         ])
        classreached = len(bearable.I2CDevice.mock_calls)
        reached = len(bear1._device.mock_calls)
        
        bear1[0] = 1.0
        ### Checking instance is not behaving as I would expect - it does not
        ### start with a per instance call_list
        self.assertEqual(bear1._device.mock_calls[reached:],
                        [call.__enter__(),
                         call.write(b'\x00\x11'),
                         call.__exit__(None, None, None),
                         call.__enter__(),
                         call.write(b'\x01\x80\x00\x00\x00\x00\x00'),
                         call.__exit__(None, None, None)
                        ])
        self.assertEqual(bearable.I2CDevice.mock_calls[classreached:],
                         [call().__enter__(),
                          call().write(b'\x00\x11'),
                          call().__exit__(None, None, None),
                          call().__enter__(),
                          call().write(b'\x01\x80\x00\x00\x00\x00\x00'),
                          call().__exit__(None, None, None)
                         ])
        if debug > 2: print(bear1._device.mock_calls[reached:])
        if debug > 2: print(bearable.I2CDevice.mock_calls)
        reached = len(bear1._device.mock_calls)
        
        bear1[0] = 0.5
        self.assertEqual(bear1._device.mock_calls[reached:],
                         [call.__enter__(),
                          call.write(b'\x01\x40\x00\x00\x00\x00\x00'),
                          call.__exit__(None, None, None)
                         ])
        if debug > 2: print(bear1._device.mock_calls[reached:])
        reached = len(bear1._device.mock_calls)

        bear1[11] = 1.0
        self.assertEqual(bear1._device.mock_calls[reached:],
                         [call.__enter__(),
                          call.write(b'\x01\x40\x00\x00\x00\x00\x08'),
                          call.__exit__(None, None, None)
                         ])
        if debug > 2: print(bear1._device.mock_calls[reached:])
        reached = len(bear1._device.mock_calls)

    def testModeAlternation(self):
        """
        Test 
        1) creation of Bearable instance,
        2) assignment to go into _BEAR_LED_DIRECT_MODE
        3) pattern() to go into _BEAR_LED_PATTERN_MODE
        4) assignment to return to _BEAR_LED_DIRECT_MODE
        """
        reached=len(bearable.I2CDevice.mock_calls)
        reached=0
        # default is auto_write=True
        badge_i2c_addr = 0x15
        bear1 = bearable.Bearable(mockedi2c)
        
        self.assertEqual(type(bear1).__name__,
                         'Bearable')
        self.assertEqual(bearable.I2CDevice.mock_calls[reached:],
                         [call(mockedi2c, badge_i2c_addr)
                         ])
        if debug > 2: print(bearable.I2CDevice.mock_calls[reached:])
        reached = len(bearable.I2CDevice.mock_calls)
        
        bear1[0] = 0.25
        self.assertEqual(bearable.I2CDevice.mock_calls[reached:],
                         [call().__enter__(),
                          call().write(b'\x00\x11'),
                          call().__exit__(None, None, None),
                          call().__enter__(),
                          call().write(b'\x01\x20\x00\x00\x00\x00\x00'),
                          call().__exit__(None, None, None)
                         ])
        if debug > 2: print(bearable.I2CDevice.mock_calls[reached:])
        reached = len(bearable.I2CDevice.mock_calls)
        
        bear1.pattern(3)
        self.assertEqual(bearable.I2CDevice.mock_calls[reached:],
                         [call().__enter__(),
                          call().write(b'\x00\x10'),
                          call().__exit__(None, None, None),
                          call().__enter__(),
                          call().write(b'\x08\x03'), 
                          call().__exit__(None, None, None)
                         ])
        if debug > 2: print(bearable.I2CDevice.mock_calls[reached:])
        reached = len(bearable.I2CDevice.mock_calls)

        bear1[6] = 1.0
        self.assertEqual(bearable.I2CDevice.mock_calls[reached:],
                         [call().__enter__(),
                          call().write(b'\x00\x11'),
                          call().__exit__(None, None, None),
                          call().__enter__(),
                          call().write(b'\x01\x20\x00\x00\x80\x00\x00'),
                          call().__exit__(None, None, None)
                         ])
        if debug > 2: print(bearable.I2CDevice.mock_calls[reached:])
        reached = len(bearable.I2CDevice.mock_calls)

    def testReadPin(self):
        """
        Test 
        1) creation of Bearable instance,
        2) first read of pin,
        3) second read of pin.
        3) third read of pin.
        """
        reached=len(bearable.I2CDevice.mock_calls)
        # default is auto_write=True
        badge_i2c_addr = 0x15
        bear1 = bearable.Bearable(mockedi2c)
        
        self.assertEqual(type(bear1).__name__,
                         'Bearable')
        self.assertEqual(bearable.I2CDevice.mock_calls[reached:],
                         [call(mockedi2c, badge_i2c_addr)
                         ])
        if debug > 2: print(__name__, bearable.I2CDevice.mock_calls[reached:])
        reached = len(bearable.I2CDevice.mock_calls)

        i2cByteVal=0x05
        def mock_readinto(buf):
            self.assertIsInstance(buf, bytearray)
            self.assertEqual(len(buf), 1)
            buf[0] = i2cByteVal
        #bearable.I2CDevice.readinto.side_effect = mock_readinto
        ### TODO - review nasty direct assignment to bear1._device
        bear1._device.readinto.side_effect = mock_readinto
        pinFirst = bear1.read_pin()
        self.assertEqual(bearable.I2CDevice.mock_calls[reached:],
                         [call().__enter__(),
                          call().write(b'\x00\x11'),
                          call().__exit__(None, None, None),
                          call().__enter__(),
                          call().write(b'\x07'),
                          ### using a side_effect curiously the args seen
                          ### in the mock_calls are based on post side_effect
                          ### execution 
##                          call().readinto(bytearray(b'\x00')),
##                          call().readinto(bytearray(b'\x05')),
###                       would prefer this checked for bytearray type
###                       but can also do that inside side_effect 
                          call().readinto(unittest.mock.ANY),
                          call().__exit__(None, None, None),
                         ])
        self.assertEqual(pinFirst,i2cByteVal)
        if debug > 2: print(__name__, bearable.I2CDevice.mock_calls[reached:])
        reached = len(bearable.I2CDevice.mock_calls)
        
        i2cByteVal=0xc9  ### RET
        pinSecond = bear1.read_pin()
        self.assertEqual(bearable.I2CDevice.mock_calls[reached:],
                         [call().__enter__(),
                          call().write(b'\x07'),
                          call().readinto(unittest.mock.ANY),
                          call().__exit__(None, None, None),
                         ])
        self.assertEqual(pinSecond,i2cByteVal)
        if debug > 2: print(__name__, bearable.I2CDevice.mock_calls[reached:])
        reached = len(bearable.I2CDevice.mock_calls)

        pinThird = bear1.read_pin()
        self.assertEqual(bearable.I2CDevice.mock_calls[reached:],
                         [call().__enter__(),
                          call().write(b'\x07'),
                          call().readinto(unittest.mock.ANY),
                          call().__exit__(None, None, None),
                         ])
        self.assertEqual(pinThird,i2cByteVal)
        if debug > 2: print(__name__, bearable.I2CDevice.mock_calls[reached:])
        reached = len(bearable.I2CDevice.mock_calls)

        bear1._device.readinto.side_effect = None

    def testReadButton(self):
        """
        Test 
        1) creation of Bearable instance,
        2) first read of button state,
        3) a second read of button.
        """
        reached=len(bearable.I2CDevice.mock_calls)
        # default is auto_write=True
        badge_i2c_addr = 0x15
        bear1 = bearable.Bearable(mockedi2c)
        
        self.assertEqual(type(bear1).__name__,
                         'Bearable')
        self.assertEqual(bearable.I2CDevice.mock_calls[reached:],
                         [call(mockedi2c, badge_i2c_addr)
                         ])
        if debug > 2: print(bearable.I2CDevice.mock_calls[reached:])
        reached = len(bearable.I2CDevice.mock_calls)

        ### TODO - mock alternating return data from i2c response to cause read_button to alternate
        ###        False, True, False, True, etc
        buttonState1 = bear1.read_button()
        self.assertEqual(bearable.I2CDevice.mock_calls[reached:reached+6],
                         [call().__enter__(),
                          call().write(b'\x00\x11'),
                          call().__exit__(None, None, None),
                          call().__enter__(),
                          call().write(b'\x00'),
                          call().__exit__(None, None, None),
                          ### TODO - code the read later when I understand more about it - remember slice 
                         ])
        if debug > 2: print(bearable.I2CDevice.mock_calls[reached:reached+6])
        reached = len(bearable.I2CDevice.mock_calls)
        
        buttonState2 = bear1.read_button()
        self.assertEqual(bearable.I2CDevice.mock_calls[reached:reached+3],
                         [call().__enter__(),
                          call().write(b'\x00'),
                          call().__exit__(None, None, None),
                          ### TODO - code the read later when I understand more about it - remember slice
                         ])
        if debug > 2: print(bearable.I2CDevice.mock_calls[reached:reached+3])
        reached = len(bearable.I2CDevice.mock_calls)


if __name__ == '__main__':
    unittest.main(verbosity=verbose)
