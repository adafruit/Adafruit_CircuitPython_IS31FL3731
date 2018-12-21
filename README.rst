Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-is31fl3731/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/is31fl3731/en/latest/
    :alt: Documentation Status

.. image :: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_IS31FL3731.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_IS31FL3731
    :alt: Build Status

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

Building locally
================

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-is31fl3731 --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
