# The MIT License (MIT)
#
# Copyright (c) 2017 Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`adafruit_is31fl3731.ScrollPhatHD`
====================================================

CircuitPython driver for the Pimoroni 17x7 Scroll pHAT HD.


* Author: David Glaude

Implementation Notes
--------------------

**Hardware:**

* `Pimoroni 17x7 Scroll pHAT HD
  <https://www.adafruit.com/product/3473>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware:
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
