# SPDX-FileCopyrightText: Tony DiCola 2017 for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_is31fl3731.led_shim`
====================================================

CircuitPython driver for the IS31FL3731 charlieplex IC.


* Author: David Glaude

Implementation Notes
--------------------

**Hardware:**

* `Pimoroni 28 RGB Led Shim
  <https://www.adafruit.com/product/3831>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from . import IS31FL3731


class LedShim(IS31FL3731):
    """Supports the LED SHIM by Pimoroni"""

    width = 28
    height = 3

    def __init__(self, i2c, address=0x75):
        super().__init__(i2c, address)

    # pylint: disable-msg=too-many-arguments
    def pixelrgb(self, x, r, g, b, blink=None, frame=None):
        """
        Blink or brightness for x-pixel

        :param x: horizontal pixel position
        :param r: red brightness value 0->255
        :param g: green brightness value 0->255
        :param b: blue brightness value 0->255
        :param blink: True to blink
        :param frame: the frame to set the pixel
        """
        super().pixel(x, 0, r, blink, frame)
        super().pixel(x, 1, g, blink, frame)
        super().pixel(x, 2, b, blink, frame)

        # pylint: disable=inconsistent-return-statements
        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-branches

    @staticmethod
    def pixel_addr(x, y):
        """Translate an x,y coordinate to a pixel index."""
        if y == 0:
            if x < 7:
                return 118 - x
            if x < 15:
                return 141 - x
            if x < 21:
                return 106 + x
            if x == 21:
                return 15
            return x - 14

        if y == 1:
            if x < 2:
                return 69 - x
            if x < 7:
                return 86 - x
            if x < 12:
                return 28 - x
            if x < 14:
                return 45 - x
            if x == 14:
                return 47
            if x == 15:
                return 41
            if x < 21:
                return x + 9
            if x == 21:
                return 95
            if x < 26:
                return x + 67
            return x + 50

        if x == 0:
            return 85
        if x < 7:
            return 102 - x
        if x < 11:
            return 44 - x
        if x < 14:
            return 61 - x
        if x == 14:
            return 63
        if x < 17:
            return 42 + x
        if x < 21:
            return x + 25
        if x == 21:
            return 111
        if x < 27:
            return x + 83
        return 93
