import time
import adafruit_is31fl3731
import board
import busio

sweep = [1, 2, 3, 4, 6, 8, 10, 15, 20, 30, 40, 60, 60, 40, 30, 20, 15, 10, 8, 6, 4, 3, 2, 1]

with busio.I2C(board.SCL, board.SDA) as i2c:
    display = adafruit_is31fl3731.CharlieWing(i2c)
    while True:
        for incr in range(24):
            for x in range(15):
                for y in range(7):
                    display.pixel(x, y, sweep[(x+y+incr)%24])
        time.sleep(.02)
