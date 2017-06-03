
Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-is31fl3731/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/is31fl3731/en/latest/
    :alt: Documentation Status

.. image :: https://badges.gitter.im/adafruit/circuitpython.svg
    :target: https://gitter.im/adafruit/circuitpython?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
    :alt: Gitter

TODO

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_
* `Register <https://github.com/adafruit/Adafruit_CircuitPython_Register>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

Matrix::

    import adafruit_is31fl3731
    import board
    import busio
    with busio.I2C(board.SCL, board.SDA) as i2c:
        display = adafruit_is31fl3731.Matrix(i2c)
        display.fill(127)


Charlie Wing::

    import adafruit_is31fl3731
    import board
    import busio
    with busio.I2C(board.SCL, board.SDA) as i2c:
        display = adafruit_is31fl3731.CharlieWing(i2c)
        display.fill(127)

        # Turn off pixel 4,4, change its brightness and turn it back on
        frame = display.displayed_frame
        frame.on[4,4] = False
        frame.brightness[4,4] = 192
        frame.on[4,4] = True

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
