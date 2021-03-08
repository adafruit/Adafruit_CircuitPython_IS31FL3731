# SPDX-FileCopyrightText: Tony DiCola 2017 for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_is31fl3731.scroll_phat_hd`
====================================================

CircuitPython driver for the Pimoroni 17x7 Scroll pHAT HD.


* Author: David Glaude

Implementation Notes
--------------------

**Hardware:**

* `Pimoroni 17x7 Scroll pHAT HD
  <https://www.adafruit.com/product/3473>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from . import IS31FL3731


class ScrollPhatHD(IS31FL3731):
    """Supports the Scroll pHAT HD by Pimoroni"""

    width = 17
    height = 7

    @staticmethod
    def pixel_addr(x, y):
        """Translate an x,y coordinate to a pixel index."""
        if x <= 8:
            x = 8 - x
            y = 6 - y
        else:
            x = x - 8
            y = y - 8
        return x * 16 + y
