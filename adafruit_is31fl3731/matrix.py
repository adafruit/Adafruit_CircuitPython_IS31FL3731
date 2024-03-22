# SPDX-FileCopyrightText: Tony DiCola 2017 for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_is31fl3731.matrix`
====================================================

CircuitPython driver for the IS31FL3731 charlieplex IC.


* Author(s): Tony DiCola, Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Hardware:**

* `Adafruit 16x9 Charlieplexed PWM LED Matrix Driver - IS31FL3731
  <https://www.adafruit.com/product/2946>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
from . import IS31FL3731

try:
    from typing import TYPE_CHECKING, List, Tuple

    if TYPE_CHECKING:
        from circuitpython_typing import ReadableBuffer
except ImportError as e:
    pass


class Matrix(IS31FL3731):
    """Charlieplexed Featherwing & IS31FL3731 I2C Modules"""

    width: int = 16
    height: int = 9

    @staticmethod
    def pixel_addr(x: int, y: int) -> int:
        """Calulate the offset into the device array for x,y pixel"""
        return x + y * 16

    # This takes precedence over image() in __init__ and is tuned for the
    # Matrix class. Some shortcuts can be taken because matrix layout is
    # very straightforward, and a few large write operations are used
    # rather than pixel-by-pixel writes, yielding significant speed gains
    # for animation. Buffering the full matrix for a quick write is not a
    # memory concern here, as by definition this method is used with PIL
    # images; we're not running on a RAM-constrained microcontroller.
    def image(self, img: str = None, blink: bool = False, frame: int = 0):
        """Set buffer to value of Python Imaging Library image.
        The image should be in 8-bit mode (L) and a size equal to the
        display size.

        :param img: Python Imaging Library image
        :param blink: True to blink
        :param frame: the frame to set the image
        """
        if img.mode != "L":
            raise ValueError("Image must be in mode L.")
        if img.size[0] != self.width or img.size[1] != self.height:
            raise ValueError(
                "Image must be same dimensions as display ({0}x{1}).".format(
                    self.width, self.height
                )
            )

        # Frame-select and then write pixel data in one big operation
        if frame is not 0:
            self._bank(frame)
        # We can safely reduce the image to a "flat" byte sequence because
        # the matrix layout is known linear; no need to go through a 2D
        # pixel array or invoke pixel_addr().
        self._i2c_write_block(bytes([0x24]) + img.tobytes())
        # Set or clear blink state if requested, for all pixels at once
        if blink:
            # 0x12 is _BLINK_OFFSET in __init__.py
            self._i2c_write_block(bytes([0x12] + [1 if blink else 0] * 18))
