# SPDX-FileCopyrightText: Tony DiCola 2017 for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_is31fl3731.RGBmatrix5x5`
====================================================

CircuitPython driver for the IS31FL3731 charlieplex IC.


* Author(s): Tony DiCola, Melissa LeBlanc-Williams, David Glaude

Implementation Notes
--------------------

**Hardware:**

* `5x5 RGB Matrix Breakout
  <https://shop.pimoroni.com/products/5x5-rgb-matrix-breakout>`_


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from . import IS31FL3731


class RGBmatrix5x5(IS31FL3731):
    """Supports the Pimoroni RGBmatrix5x5 with 5x5 matrix of RGB LEDs """

    width = 25
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

        super().pixel(x, 0, g, blink, frame)
        super().pixel(x, 1, r, blink, frame)
        super().pixel(x, 2, b, blink, frame)

        # pylint: disable=inconsistent-return-statements
        # pylint: disable=too-many-return-statements
        # pylint: disable=too-many-branches

    @staticmethod
    def pixel_addr(x, y):
        # pylint: disable=duplicate-code
        lookup = [
            (118, 69, 85),
            (117, 68, 101),
            (116, 84, 100),
            (115, 83, 99),
            (114, 82, 98),
            (113, 81, 97),
            (112, 80, 96),
            (134, 21, 37),
            (133, 20, 36),
            (132, 19, 35),
            (131, 18, 34),
            (130, 17, 50),
            (129, 33, 49),
            (128, 32, 48),
            (127, 47, 63),
            (121, 41, 57),
            (122, 25, 58),
            (123, 26, 42),
            (124, 27, 43),
            (125, 28, 44),
            (126, 29, 45),
            (15, 95, 111),
            (8, 89, 105),
            (9, 90, 106),
            (10, 91, 107),
            (11, 92, 108),
            (12, 76, 109),
            (13, 77, 93),
        ]

        return lookup[x][y]
