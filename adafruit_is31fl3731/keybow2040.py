# SPDX-FileCopyrightText: Tony DiCola 2017 for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_is31fl3731.keybow2040`
====================================================

CircuitPython driver for the IS31FL3731 charlieplex IC.


* Author(s): Tony DiCola, Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Hardware:**

* `Pimoroni Keybow 2040
  <https://shop.pimoroni.com/products/keybow-2040>`_


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from . import IS31FL3731


class Keybow2040(IS31FL3731):
    """Supports the Pimoroni Keybow 2040 with 4x4 matrix of RGB LEDs"""

    width = 16
    height = 3

    # pylint: disable=too-many-arguments

    def pixelrgb(self, x, y, r, g, b, blink=None, frame=None):
        """
        Blink or brightness for x, y-pixel

        :param x: horizontal pixel position
        :param y: vertical pixel position
        :param r: red brightness value 0->255
        :param g: green brightness value 0->255
        :param b: blue brightness value 0->255
        :param blink: True to blink
        :param frame: the frame to set the pixel
        """
        x = (4 * (3 - x)) + y

        super().pixel(x, 0, r, blink, frame)
        super().pixel(x, 1, g, blink, frame)
        super().pixel(x, 2, b, blink, frame)

        # pylint: disable=inconsistent-return-statements
        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-branches

    @staticmethod
    def pixel_addr(x, y):

        lookup = [
            (120, 88, 104),  # 0, 0
            (136, 40, 72),  # 1, 0
            (112, 80, 96),  # 2, 0
            (128, 32, 64),  # 3, 0
            (121, 89, 105),  # 0, 1
            (137, 41, 73),  # 1, 1
            (113, 81, 97),  # 2, 1
            (129, 33, 65),  # 3, 1
            (122, 90, 106),  # 0, 2
            (138, 25, 74),  # 1, 2
            (114, 82, 98),  # 2, 2
            (130, 17, 66),  # 3, 2
            (123, 91, 107),  # 0, 3
            (139, 26, 75),  # 1, 3
            (115, 83, 99),  # 2, 3
            (131, 18, 67),  # 3, 3
        ]

        return lookup[x][y]
