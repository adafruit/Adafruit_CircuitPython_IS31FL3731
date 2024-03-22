# SPDX-FileCopyrightText: 2024 DJDevon3
# SPDX-License-Identifier: MIT
""" Adafruit 16x9 Charlieplexed PWM LED Matrix Example """

import board
import adafruit_framebuf

from adafruit_is31fl3731.matrix import Matrix as Display

# Uncomment for Pi Pico
# import busio
# i2c = busio.I2C(board.GP21, board.GP20)

i2c = board.STEMMA_I2C()
display = Display(i2c, address=0x74)

pixel_rotation = 90  # display rotation (0,90,180,270)
pixel_brightness = 20  # values (0-255)
pixel_blink = False  # blink entire display

text_to_show = "Hello World!"  # Scrolling marquee text

print(f"Display Dimensions: {display.width}x{display.height}")
print(f"Text: {text_to_show}")

# Create a framebuffer for our display
buf = bytearray(32)  # 2 bytes tall x 16 wide = 32 bytes (9 bits is 2 bytes)
buffer = adafruit_framebuf.FrameBuffer(
    buf, display.width, display.height, adafruit_framebuf.MVLSB
)

frame = 0  # start with frame 0
while True:
    # Looping marquee
    for i in range(len(text_to_show) * 9):
        buffer.fill(0)
        buffer.text(text_to_show, -i + display.width, 0, color=1)
        display.frame(frame, show=False)
        display.fill(0)
        for x in range(display.width):
            # using the FrameBuffer text result
            bite = buf[x]
            for y in range(display.height):
                bit = 1 << y & bite
                # if bit > 0 then set the pixel brightness
                if bit:
                    display.pixel(
                        x, y, pixel_brightness, blink=pixel_blink, rotate=pixel_rotation
                    )
