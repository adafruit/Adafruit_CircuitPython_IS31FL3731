# SPDX-FileCopyrightText: Tony DiCola 2017 for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_is31fl3731.charlie_bonnet`
====================================================

CircuitPython driver for the IS31FL3731 charlieplex IC.


* Author(s): Tony DiCola, Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Hardware:**

* `Pimoroni 11x7 LED Matrix Breakout <https://shop.pimoroni.com/products/11x7-led-matrix-breakout>`_


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from . import IS31FL3731


class Matrix11x7(IS31FL3731):
    """Supports the 11x7 LED Matrix Breakout by Pimoroni"""

    width = 11
    height = 7

    def __init__(self, i2c, address=0x75):
        super().__init__(i2c, address)

    @staticmethod
    def pixel_addr(x, y):
        """Translate an x,y coordinate to a pixel index."""
        return (x << 4) - y + (6 if x <= 5 else -82)
