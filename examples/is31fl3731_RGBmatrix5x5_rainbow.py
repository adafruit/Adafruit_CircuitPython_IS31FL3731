# SPDX-FileCopyrightText: 2021 Sandy Macdonald, David Glaude
# SPDX-License-Identifier: MIT

"""
Example to display a rainbow animation on the 5x5 RGB Matrix Breakout.

Usage:
Rename this file code.py and pop it on your Raspberry Pico's
CIRCUITPY drive.

This example is for use on the Pico Explorer Base or other board that use the same SDA/SCL pin.

Author(s): Sandy Macdonald, David Glaude.
"""

import time
import math
import board

from adafruit_is31fl3731.RGBmatrix5x5 import RGBmatrix5x5 as Display

# pylint: disable=inconsistent-return-statements
# pylint: disable=too-many-return-statements
# pylint: disable=invalid-name


def hsv_to_rgb(hue, sat, val):
    """
    Convert HSV colour to RGB

    :param hue: hue; 0.0-1.0
    :param sat: saturation; 0.0-1.0
    :param val: value; 0.0-1.0
    """

    if sat == 0.0:
        return (val, val, val)

    i = int(hue * 6.0)

    p = val * (1.0 - sat)
    f = (hue * 6.0) - i
    q = val * (1.0 - sat * f)
    t = val * (1.0 - sat * (1.0 - f))

    i %= 6

    if i == 0:
        return (val, t, p)
    if i == 1:
        return (q, val, p)
    if i == 2:
        return (p, val, t)
    if i == 3:
        return (p, q, val)
    if i == 4:
        return (t, p, val)
    if i == 5:
        return (val, p, q)


# Create the I2C bus on a Pico Explorer Base
i2c = busio.I2C(board.GP21, board.GP20)

# Set up 5x5 RGB matrix Breakout
display = adafruit_is31fl3731.RGBmatrix5x5(i2c)

step = 0

while True:
    step += 1
    for y in range(0, 5):
        for x in range(0, 5):
            pixel_hue = (x + y + (step / 20)) / 8
            pixel_hue = pixel_hue - int(pixel_hue)
            pixel_hue += 0
            pixel_hue = pixel_hue - math.floor(pixel_hue)

            rgb = hsv_to_rgb(pixel_hue, 1, 1)

            display.pixelrgb(
                x, y, int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
            )

    time.sleep(0.01)
