import board
import busio
import adafruit_is31fl3731
import time

i2c = busio.I2C(board.SCL, board.SDA)

# initialize display using Feather CharlieWing LED 15 x 7
#display = adafruit_is31fl3731.CharlieBonnet(i2c, address=0x75)

# uncomment next line if you are using Pimoroni LED SHIM
#display = adafruit_is31fl3731.LedShim(i2c, address=0x75)
display = adafruit_is31fl3731.LedShim(i2c)

# uncomment next line if you are using Adafruit 16x8 Charlieplexed Bonnet
# display = adafruit_is31fl3731.CharlieBonnet(i2c)

# initial display using Pimoroni Scroll Phat HD LED 17 x 7
# display = adafruit_is31fl3731.ScrollPhatHD(i2c)

rainbow=[
(255, 0, 0) ,
(255, 54, 0) ,
(255, 109, 0) ,
(255, 163, 0) ,
(255, 218, 0) ,
(236, 255, 0) ,
(182, 255, 0) ,
(127, 255, 0) ,
(72, 255, 0) ,
(18, 255, 0) ,
(0, 255, 36) ,
(0, 255, 91) ,
(0, 255, 145) ,
(0, 255, 200) ,
(0, 255, 255) ,
(0, 200, 255) ,
(0, 145, 255) ,
(0, 91, 255) ,
(0, 36, 255) ,
(18, 0, 255) ,
(72, 0, 255) ,
(127, 0, 255) ,
(182, 0, 255) ,
(236, 0, 255) ,
(255, 0, 218) ,
(255, 0, 163) ,
(255, 0, 109) ,
(255, 0, 54)]

while True:
    for offset in range(28):
        for x in range(28):
            r,g,b = rainbow[(x+offset)%28]
            display.pixelrgb(x, r, g, b)