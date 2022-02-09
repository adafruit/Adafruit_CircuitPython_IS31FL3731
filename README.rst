Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-is31fl3731/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/is31fl3731/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3731/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_IS31FL3731/actions/
    :alt: Build Status

CircuitPython driver for the IS31FL3731 charlieplex IC.

This driver supports the following hardware:

* `Adafruit 16x9 Charlieplexed PWM LED Matrix Driver - IS31FL3731 <https://www.adafruit.com/product/2946>`_
* `Adafruit 15x7 CharliePlex LED Matrix Display FeatherWings <https://www.adafruit.com/product/2965>`_
* `Adafruit 16x8 CharliePlex LED Matrix Bonnets <https://www.adafruit.com/product/4127>`_
* `Pimoroni 17x7 Scroll pHAT HD <https://www.adafruit.com/product/3473>`_
* `Pimoroni 28x3 (r,g,b) Led Shim <https://www.adafruit.com/product/3831>`_
* `Pimoroni Keybow 2040 with 4x4 matrix of RGB LEDs <https://shop.pimoroni.com/products/keybow-2040>`_
* `Pimoroni 5x5 RGB Matrix Breakout <https://shop.pimoroni.com/products/5x5-rgb-matrix-breakout>`_


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-is31fl3731/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-is31fl3731

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-is31fl3731

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-is31fl3731

Usage Example
=============

Matrix:

.. code:: python

    from adafruit_is31fl3731.matrix import Matrix
    import board
    import busio
    with busio.I2C(board.SCL, board.SDA) as i2c:
        display = Matrix(i2c)
        display.fill(127)


Charlie Wing:

.. code:: python

    from adafruit_is31fl3731.charlie_wing import CharlieWing
    import board
    import busio
    with busio.I2C(board.SCL, board.SDA) as i2c:
        display = CharlieWing(i2c)
        display.fill(127)

        # Turn off pixel 4,4, change its brightness and turn it back on
        display.pixel(4, 4, 0)   # Turn off.
        display.pixel(4, 4, 50)  # Low brightness (50)
        display.pixel(4, 4, 192) # Higher brightness (192)

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/is31fl3731/en/latest/>`_.

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_is31fl3731/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
