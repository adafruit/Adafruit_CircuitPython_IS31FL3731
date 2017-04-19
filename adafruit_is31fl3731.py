# The MIT License (MIT)
#
# Copyright (c) 2016 Radomir Dopieralski
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries
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
`adafruit_is31fl3731`
====================================================

Basic driver for the IS31FL3731 a charlieplexed LED driver.

* Author(s): Radomir Dopieralski, Scott Shawcroft
* Datasheet: http://www.issi.com/WW/pdf/31FL3731.pdf
"""

import math
import time

from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register import i2c_bit
from adafruit_register import i2c_bits
from adafruit_register import i2c_struct

_FRAME_REGISTER = const(0x01)
_AUTOPLAY1_REGISTER = const(0x02)
_AUTOPLAY2_REGISTER = const(0x03)
_BLINK_REGISTER = const(0x05)
_AUDIOSYNC_REGISTER = const(0x06)
_BREATH1_REGISTER = const(0x08)
_BREATH2_REGISTER = const(0x09)
_SHUTDOWN_REGISTER = const(0x0a)
_GAIN_REGISTER = const(0x0b)
_ADC_REGISTER = const(0x0c)

_CONFIG_BANK = const(0x0b)
_BANK_ADDRESS = const(0xfd)

_PICTURE_MODE = const(0x00)
_AUTOPLAY_MODE = const(0x08)
_AUDIOPLAY_MODE = const(0x18)

class ByteArray:
    """Provides byte access via a 2D array using index like [1,2] where 1 is x and 2 is y."""
    def __init__(self, parent, frame, register):
        self.parent = parent
        self.register = register
        self.buf = bytearray(2)
        self.frame = frame

    def __getitem__(self, index):
        addr = self.parent._pixel_addr(*index)
        self.parent.edit_frame = self.frame

        with self.parent.i2c_device as i2c:
            self.buf[0] = self.register + addr
            i2c.write(self.buf, end=1)
            i2c.read_into(self.buf[0], start=1)

        return self.buf[1]

    def __setitem__(self, index, val):
        addr = self.parent._pixel_addr(*index)
        self.parent.edit_frame = self.frame

        with self.parent.i2c_device as i2c:
            self.buf[0] = self.register + addr
            self.buf[1] = val
            i2c.write(self.buf)

class BitArray:
    """Provides bit access via a 2D array using index like [1,2] where 1 is x and 2 is y."""
    def __init__(self, parent, frame, register):
        self.parent = parent
        self.register = register
        self.buf = bytearray(2)
        self.frame = frame

    def _read_bits(self, index):
        addr = self.parent._pixel_addr(*index)
        addr //= 8
        self.parent.edit_frame = self.frame

        with self.parent.i2c_device as i2c:
            self.buf[0] = self.register + addr
            i2c.write(self.buf, end=1)
            i2c.read_into(self.buf, start=1)
        return self.buf[1]

    def __getitem__(self, index):
        return (self._read_bits(index) & (1 << bit)) != 0

    def __setitem__(self, index, val):
        addr = self.parent._pixel_addr(*index)
        bit = addr % 8
        addr //= 8

        bits = self._read_bits(index)
        if val:
            bits |= 1 << bit
        else:
            bits &= ~(1 << bit)

        with self.parent.i2c_device as i2c:
            self.buf[0] = self.register + addr
            self.buf[1] = bits
            i2c.write(self.buf)

import time

class Frame:
    def __init__(self, parent):
        self.parent = parent
        self.brightness = ByteArray(parent, self, 0x24)
        """Pixel array model after pixel arrays in PIL"""
        self.on = BitArray(parent, self, 0x0)
        self.blink = BitArray(parent, self, 0x12)

    def fill(self, color, blink=False):
        self.parent.edit_frame = self
        # TODO(tannewt): Bulk fill brightness and blink for speed.
        # TODO(tannewt): Turn on each pixel once at the start.
        for y in range(4):
            for x in range(4):
                self.on[x,y] = True
                self.brightness[x,y] = color
                self.blink[x,y] = blink

class Matrix:
    """Charlieplexed 16x9 LED matrix."""
    width = 16
    height = 9

    # Known as the shutdown register but 1 is on and 0 is shutdown.
    _on = i2c_bit.RWBit(_SHUTDOWN_REGISTER, 0)
    """Whether the display is on."""

    _bank = i2c_struct.UnaryStruct(_BANK_ADDRESS, "B")
    _blink_period_time = i2c_bits.RWBits(3, 0x5, 0)
    _blink_enable = i2c_bit.RWBit(0x5, 0)
    _mode = i2c_bits.RWBits(2, 0x0, 0x3)

    # TODO(tannewt): Support autoplay and breath animations. Perhaps use a
    # separate module with subclasses to reduce memory footprint.

    def __init__(self, i2c, address=0x74):
        self.i2c_device = I2CDevice(i2c, address)
        # Cache the active frame/bank to reduce I2C traffic.
        self._bank_cache = 9
        self.edit_frame = None

        # Turn off LED outputs
        self._on = False

        # Setup the registers
        self._mode = _PICTURE_MODE
        self.frames = []
        for i in range(8):
            frame = Frame(self)
            self.frames.append(frame)

            # Blank out the frame memory.
            self.edit_frame = frame
            zeroes = bytearray(0xb3 + 1)
            with self.i2c_device as i2c:
                i2c.write(zeroes)
        self.displayed_frame = self.frames[0]

        # Turn on the display
        self.edit_frame = None
        self._on = True

    @property
    def edit_frame(self):
        """Current frame being edited. None if config."""
        if self._bank_cache == _CONFIG_BANK:
            return None
        return self.frames[self._bank_cache]

    @edit_frame.setter
    def edit_frame(self, frame):
        bank = _CONFIG_BANK
        if frame != None:
            bank = self.frames.index(frame)

        if self._bank_cache != bank:
            self._bank_cache = bank
            self._bank = bank

    @property
    def blink_period(self):
        """Blink period up to 1890ms in steps of 270ms."""
        self.edit_frame = None
        return self._blink_period * 270

    @blink_period.setter
    def blink_period(self, period):
        period //= 270
        self.edit_frame = None
        self._blink_period = period

    def _pixel_addr(self, x, y):
        return x + y * 16

class CharlieWing(Matrix):
    """Driver for the 15x7 CharlieWing Adafruit FeatherWing."""
    width = 15
    height = 7

    def _pixel_addr(self, x, y):
        if x > 7:
            x = 15 - x
            y += 8
        else:
            y = 7 - y
        return x * 16 + y
