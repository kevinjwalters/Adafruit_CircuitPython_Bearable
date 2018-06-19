Introduction
============

.. COMMENT .. image:: https://readthedocs.org/projects/circuitpython-bearable/badge/?version=latest
.. COMMENT     :target: https://circuitpython.readthedocs.io/projects/bearable/en/latest/
.. COMMENT     :alt: Documentation Status

.. COMMENT .. image:: https://img.shields.io/discord/327254708534116352.svg
.. COMMENT     :target: https://discord.gg/nBQh6qu
.. COMMENT     :alt: Discord

.. COMMENT .. image:: https://travis-ci.org/adafruit/Adafruit_CircuitPython_Bearable.svg?branch=master
.. COMMENT     :target: https://travis-ci.org/adafruit/Adafruit_CircuitPython_Bearable
.. COMMENT     :alt: Build Status

Driver for the Pimoroni Bearable(s) bear and fox badges using i2c pads.
The twelve LEDs are presented as a sequence allowing direct assignment where the brightness
is represented by a real number up to 1.0.
The sensor input can also be read and returns an integer between 0-255.


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

This example demonstrates setting the brightness on pixels and reading the sensor value,
the pins in this case are for the `Gemma M0 <https://www.adafruit.com/product/3501>`_.

.. code-block:: python

    import board
    import busio
    import time
    import bearable
    
    i2c = busio.I2C(board.D2, board.D0, frequency = 100*1000)
    bear = bearable.Bearable(i2c)
    brightness = 1.0 

    for i in range(20):
        bear.fill(brightness)
        print('sensor input is {:d}'.format(bear.read_pin()))
        brightness = 1.0 - brightness
        time.sleep(0.5)
    bear.pattern(10)   # three spinning

Contributing
============

Contributions are welcome!

.. COMMENT Building locally
.. COMMENT ================
.. COMMENT 
.. COMMENT Zip release files
.. COMMENT -----------------
.. COMMENT 
.. COMMENT To build this library locally you'll need to install the
.. COMMENT `circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.
.. COMMENT 
.. COMMENT .. code-block:: shell
.. COMMENT 
.. COMMENT     python3 -m venv .env
.. COMMENT     source .env/bin/activate
.. COMMENT     pip install circuitpython-build-tools
.. COMMENT 
.. COMMENT Once installed, make sure you are in the virtual environment:
.. COMMENT 
.. COMMENT .. code-block:: shell
.. COMMENT 
.. COMMENT     source .env/bin/activate
.. COMMENT 
.. COMMENT Then run the build:
.. COMMENT 
.. COMMENT .. code-block:: shell
.. COMMENT 
.. COMMENT     circuitpython-build-bundles --filename_prefix circuitpython-bearable --library_location .
.. COMMENT 
.. COMMENT Sphinx documentation
.. COMMENT -----------------------
.. COMMENT 
.. COMMENT Sphinx is used to build the documentation based on rST files and comments in the code. First,
.. COMMENT install dependencies (feel free to reuse the virtual environment from above):
.. COMMENT 
.. COMMENT .. code-block:: shell
.. COMMENT 
.. COMMENT     python3 -m venv .env
.. COMMENT     source .env/bin/activate
.. COMMENT     pip install Sphinx sphinx-rtd-theme
.. COMMENT 
.. COMMENT Now, once you have the virtual environment activated:
.. COMMENT 
.. COMMENT .. code-block:: shell
.. COMMENT 
.. COMMENT     cd docs
.. COMMENT     sphinx-build -E -W -b html . _build/html
.. COMMENT 
.. COMMENT This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
.. COMMENT view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
.. COMMENT locally verify it will pass.
