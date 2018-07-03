
### TODO - i still don't understand how to replace each method in a mocked class
### TODO - call checks - how to test for any object?

import unittest
from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import call

import sys
# NOT NEEDED sys.modules['adafruit_bus_device'] = Mock()
#### MagicMock needed to deal with __enter__ and __exit__
sys.modules['adafruit_bus_device.i2c_device'] = MagicMock()
sys.modules['busio'] = Mock()

# there may be neater way to do this
if hasattr(__builtins__, 'absasdfsadf'):
    pass
else:
    __builtins__.const = lambda x: x

import bearable

import busio
import bearable

#class MockI2C:
#    def __enter__():
#        print('__enter__')
#
#    def __exit__():
#        print('__exit__')
#
#    def write():
#        print('write')
#
#    def readinto():
#        print('readinto')

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
reached=0

# default is auto_write=True
bear1 = bearable.Bearable(mockedi2c)

if type(bear1).__name__ == "Bearable":
    print('all is well')
print(bearable.I2CDevice.mock_calls[reached:] == [call(666, 21)])

### elements are <class 'unittest.mock._Call'>
print(bearable.I2CDevice.mock_calls[reached:])
reached=len(bearable.I2CDevice.mock_calls)

bear1[0] = 1.0

print(bearable.I2CDevice.mock_calls[reached:] == [call().__enter__(), call().write(b'\x00\x11'), call().__exit__(None, None, None), call().__enter__(), call().write(b'\x01\x80\x00\x00\x00\x00\x00'), call().__exit__(None, None, None)])

### elements are <class 'unittest.mock._Call'>
print(bearable.I2CDevice.mock_calls[reached:])
reached=len(bearable.I2CDevice.mock_calls)

bear1[1] = 1.0
print(bearable.I2CDevice.mock_calls[reached:] == [call().__enter__(), call().write(b'\x01\x88\x00\x00\x00\x00\x00'), call().__exit__(None, None, None)])

### elements are <class 'unittest.mock._Call'>
print(bearable.I2CDevice.mock_calls[reached:])
reached=len(bearable.I2CDevice.mock_calls)


print('goodbye from test')
