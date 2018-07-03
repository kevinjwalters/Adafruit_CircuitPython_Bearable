
import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock

import sys
sys.modules['adafruit_bus_device'] = Mock()
sys.modules['adafruit_bus_device.i2c_device'] = Mock()
sys.modules['busio'] = Mock()

### TODO - need to create I2CDevice 
# there may be neater way to do this
if hasattr(__builtins__, 'absasdfsadf'):
    pass
else:
    __builtins__.const = lambda x: x

import bearable

import busio
import bearable

class MockI2C:
    def __enter__():
        print('__enter__')

    def __exit__():
        print('__exit__')

    def write():
        print('write')

    def readinto():
        print('readinto')

#sclpin = board.D2
#dapin = board.D0
# i2c = busio.I2C(sclpin, sdapin, frequency = 100*1000)
#mockedi2c = Mock(spec=MockI2C, side_effect=print('WORD'))
#mockedi2c = Mock(spec=MockI2C)  does not do what I thought it did
mockedi2c = Mock()

### This proves technique works but needs to be applied to the I2CDevice in
### bearable

#mockedi2c.__enter__ = lambda a : print('__enter__')
#mockedi2c.__exit__  = lambda a, b, c, d  : print('__exit__')
#mockedi2c.__exit__.return_value = False
#mockedi2c.write     = lambda buf : print('write:' + ''.join(format(x, '02x') for x in buf))
#mockedi2c.readinto  = lambda buf : print('readinto:' + ''.join(format(x, '02x') for x in buf))

buf = bytearray(4)
buf[:] = map(ord,['A', 'B', 'C', 'D'])

#with mockedi2c:
#    mockedi2c.write(buf)

#with mockedi2c:
#    mockedi2c.readinto(buf)

# needs write and readinto

print('welcome to test')

# default is auto_write=True
bear1 = bearable.Bearable(mockedi2c)
if type(bear1).__name__ == "Bearable":
    print('all is well')

bear1[0] = 1.0

print('goodbye from test')
