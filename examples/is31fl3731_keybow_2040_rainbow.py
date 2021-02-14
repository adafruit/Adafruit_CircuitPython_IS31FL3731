# SPDX-FileCopyrightText: 2021 Sandy Macdonald
# SPDX-License-Identifier: MIT

import time
import math
import board
import busio

import adafruit_is31fl3731

i2c = busio.I2C(board.GP5, board.GP4)

# Set up 4x4 RGB matrix of Keybow 2040
display = adafruit_is31fl3731.Keybow2040(i2c)

def hsv_to_rgb(h, s, v):
    """
    Convert HSV colour to RGB

    :param h: hue; 0.0-1.0
    :param s: saturation; 0.0-1.0
    :param v: value; 0.0-1.0
    """
    if s == 0.0:
        return (v, v, v)
    
    i = int(h * 6.0)

    f = (h * 6.0) - i
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    i %= 6
    
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)

i = 0
while True:
    i = i + 1
    for y in range(0, 4):
        for x in range(0, 4):            
            hue = (x + y + (i / 20)) / 8
            hue = hue - int(hue)
            hue += 0
            hue = hue - math.floor(hue)
            
            rgb = hsv_to_rgb(hue, 1, 1)
            
            display.pixelrgb(x, y, int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
            
    time.sleep(0.01)
