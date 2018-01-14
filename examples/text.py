import board
import busio
import framebuf
import adafruit_is31fl3731

buf = bytearray(32)

with busio.I2C(board.SCL, board.SDA) as i2c:
    # initial display using Feather CharlieWing LED 15 x 7
    display = adafruit_is31fl3731.CharlieWing(i2c)
    # uncomment line if you are using Adafruit 16x9 Charlieplexed PWM LED Matrix
    #display = adafruit_is31fl3731.Matrix(i2c)
    fb = framebuf.FrameBuffer(buf, display.width, display.height, framebuf.MONO_VLSB)
    text_to_show = "Adafruit!!"

    while True:
        for i in range(len(text_to_show) * 9):
            fb.fill(0)
            fb.text(text_to_show, -i + display.width, 0)

            for x in range(display.width):
                bite = buf[x]
                for y in range(display.height):
                    bit = 1 << y & bite
                    display.pixel(x, y, 50 if bit else 0)
