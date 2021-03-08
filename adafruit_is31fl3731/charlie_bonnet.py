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

* `Adafruit 16x8 CharliePlex LED Matrix Bonnets
  <https://www.adafruit.com/product/4127>`_


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from . import IS31FL3731


class CharlieBonnet(IS31FL3731):
    """Supports the Charlieplexed bonnet"""

    width = 16
    height = 8

    @staticmethod
    def pixel_addr(x, y):
        """Calulate the offset into the device array for x,y pixel"""
        if x >= 8:
            return (x - 6) * 16 - (y + 1)
        return (x + 1) * 16 + (7 - y)
