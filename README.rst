Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-is31fl3731/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/is31fl3731/en/latest/
    :alt: Documentation Status

.. image :: https://badges.gitter.im/adafruit/circuitpython.svg
    :target: https://gitter.im/adafruit/circuitpython?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
    :alt: Gitter

CircuitPython driver for the IS31FL3731 charlieplex IC.

This driver supports the following hardware:

* `Adafruit 16x9 Charlieplexed PWM LED Matrix Driver - IS31FL3731 <https://www.adafruit.com/product/2946>`_
* `Adafruit 15x7 CharliePlex LED Matrix Display FeatherWings <https://www.adafruit.com/product/2965>`_

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

Matrix:

.. code:: python

    import adafruit_is31fl3731
    import board
    import busio
    with busio.I2C(board.SCL, board.SDA) as i2c:
        display = adafruit_is31fl3731.Matrix(i2c)
        display.fill(127)


Charlie Wing:

.. code:: python

    import adafruit_is31fl3731
    import board
    import busio
    with busio.I2C(board.SCL, board.SDA) as i2c:
        display = adafruit_is31fl3731.CharlieWing(i2c)
        display.fill(127)

        # Turn off pixel 4,4, change its brightness and turn it back on
        display.pixel(4, 4, 0)   # Turn off.
        display.pixel(4, 4, 50)  # Low brightness (50)
        display.pixel(4, 4, 192) # Higher brightness (192)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_is31fl3731/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

API Reference
=============

.. toctree::
   :maxdepth: 2

   api
