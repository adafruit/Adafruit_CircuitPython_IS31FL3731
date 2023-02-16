# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from adafruit_is31fl3731.led_shim import LedShim as Display

i2c = busio.I2C(board.SCL, board.SDA)

# initial display if you are using Pimoroni LED SHIM
display = Display(i2c)

y = 1
for x in range(28):
    display.pixel(x, y, 255)


try:
    display.fade(fade_in=100, pause=26)
    while True:
        time.sleep(1)
except:
    display.sleep(True)
    exit
