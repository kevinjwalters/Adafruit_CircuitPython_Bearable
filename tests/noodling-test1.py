
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

import os
debug = int(os.getenv('BEARDEBUG',0))
verbose = int(os.getenv('BEARVERBOSE',2))

import sys
### Need to learn more about patch to determine optimal
### way to mock I2CDevice in adafruit_bus_device.i2c_device
#### MagicMock needed to deal with __enter__ and __exit__
sys.modules['adafruit_bus_device.i2c_device'] = MagicMock()
sys.modules['busio'] = Mock()

# there may be neater way to do this
if hasattr(__builtins__, 'const'):
    pass
else:
    __builtins__.const = lambda x: x

import bearable

import busio
import bearable

### TODO - move this into TestI2cComms ?
# create a mocked busio.I2C(sclpin, sdapin, frequency = 100*1000)
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

if __name__ == '__main__':
    unittest.main(verbosity=verbose)
