import math


_MODE_REGISTER = const(0x00)
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

_ENABLE_OFFSET = const(0x00)
_BLINK_OFFSET = const(0x12)
_COLOR_OFFSET = const(0x24)

class Matrix:
    def __init__(self, width, height, i2c, address=0x74):
        """
        Driver for the IS31FL3731 charlieplexed LED matrix.

        >>> import is31fl3731
        >>> from machine import I2C, Pin
        >>> i2c = I2C(Pin(5), Pin(4))
        >>> display = is31fl3731.Matrix(16, 9, i2c)
        >>> display.fill(127)
        >>> display.show()
        """
        self.width = width
        self.height = height
        self.i2c = i2c
        self.address = address
        self.init()

    def _bank(self, bank=None):
        if bank is None:
            return self.i2c.readfrom_mem(self.address, _BANK_ADDRESS, 1)[0]
        self.i2c.writeto_mem(self.address, _BANK_ADDRESS, bytearray([bank]))

    def _register(self, bank, register, value=None):
        self._bank(bank)
        if value is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        self.i2c.writeto_mem(self.address, register, bytearray([value]))

    def _mode(self, mode=None):
        return self._register(_CONFIG_BANK, _MODE_REGISTER, mode)

    def init(self):
        """Initialize the display."""
        self._mode(_PICTURE_MODE)
        self.frame(0)
        self.fill(0)
        for frame in range(8):
            for col in range(18):
                self._register(frame, _ENABLE_OFFSET + col, 0xff)
        self.audio_sync(False)

    def sleep(self, value):
        """Enables, disables or gets the sleep mode."""
        return self._register(_CONFIG_BANK, _SHUTDOWN_REGISTER, value)

    def autoplay(self, delay=0, loops=0, frames=0):
        """
        Enables or disables autoplay.

        If ``delay`` is 0, autoplay is disabled. Otherwise the display will
        switch between ``frames`` frames every ``delay`` milliseconds, and
        repeat the cycle ``loops`` times.  If ``loops`` is 0, it will repeat
        indefinitely.
        """
        if delay == 0:
            self._mode(_PICTURE_MODE)
            return
        delay //= 11
        if not 0 <= loops <= 7:
            raise ValueError("Loops out of range")
        if not 0 <= frames <= 7:
            raise ValueError("Frames out of range")
        if not 1 <= delay <= 64:
            raise ValueError("Delay out of range")
        self._register(_CONFIG_BANK, _AUTOPLAY1_REGISTER, loops << 4 | frames)
        self._register(_CONFIG_BANK, _AUTOPLAY2_REGISTER, delay % 64)
        self._mode(_AUTOPLAY_MODE | self._frame)

    def fade(self, fade_in=None, fade_out=None, pause=0):
        """
        Disables or enables and configures fading.

        If called without parameters, disables fading. If ``fade_in`` and/or
        ``fade_out`` are specified, it will take that many milliseconds to
        change between frames, with ``pause`` milliseconds of dark between.
        """
        if fade_in is None and fade_out is None:
            self._register(_CONFIG_BANK, _BREATH2_REGISTER, 0)
        elif fade_in is None:
            fade_in = fade_out
        elif fade_out is None:
            fade_out = fade_in
        fade_in = int(math.log(fade_in / 26, 2))
        fade_out = int(math.log(fade_out / 26, 2))
        pause = int(math.log(pause / 26, 2))
        if not 0 <= fade_in <= 7:
            raise ValueError("Fade in out of range")
        if not 0 <= fade_out <= 7:
            raise ValueError("Fade out out of range")
        if not 0 <= pause <= 7:
            raise ValueError("Pause out of range")
        self._register(_CONFIG_BANK, _BREATH1_REGISTER, fade_out << 4 | fade_in)
        self._register(_CONFIG_BANK, _BREATH2_REGISTER, 1 << 4 | pause)

    def frame(self, frame=None, show=True):
        """
        Change or get active frame.

        If ``frame`` is not specified, returns the active frame, otherwise sets
        it to the value of ``frame``. If ``show`` is ``True``, also shows that
        frame.
        """
        if frame is None:
            return self._frame
        if not 0 <= frame <= 8:
            raise ValueError("Frame out of range")
        self._frame = frame
        if show:
            self._register(_CONFIG_BANK, _FRAME_REGISTER, frame);

    def audio_sync(self, value=None):
        """Enable, disable or get sync of brightness with audio input."""
        return self._register(_CONFIG_BANK, _AUDIOSYNC_REGISTER, value)

    def audio_play(self, sample_rate, audio_gain=0,
                   agc_enable=False, agc_fast=False):
        """
        Enable or disable frame display according to the audio input.

        The ``sample_rate`` specifies sample rate in microseconds. If it is 0,
        disable the audio play. The ``audio_gain`` specifies amplification
        between 0dB and 21dB.
        """
        if sample_rate == 0:
            self._mode(_PICTURE_MODE)
            return
        sample_rate //= 46
        if not 1 <= sample_rate <= 256:
            raise ValueError("Sample rate out of range")
        self._register(_CONFIG_BANK, _ADC_REGISTER, sample_rate % 256)
        audio_gain //= 3
        if not 0 <= audio_gain <= 7:
            raise ValueError("Audio gain out of range")
        self._register(_CONFIG_BANK, _GAIN_REGISTER,
                       bool(agc_enable) << 3 | bool(agc_fast) << 4 | audio_gain)
        self._mode(_AUDIOPLAY_MODE)

    def blink(self, rate=None):
        """Get or set blink rate."""
        if rate is None:
            return (self._register(_CONFIG_BANK, _BLINK_REGISTER) & 0x07) * 270
        elif rate == 0:
            self._register(_CONFIG_BANK, _BLINK_OFFSET, 0x00)
            return
        rate //= 270
        self._register(_CONFIG_BANK, _BLINK_OFFSET, rate | 0x08)

    def fill(self, color=0, frame=None):
        """Fill the display with specified color."""
        if not 0 <= color <= 255:
            raise ValueError("Color out of range")
        if frame is None:
            frame = self._frame
        self._bank(frame)
        data = bytearray([color] * 24)
        for row in range(6):
            self.i2c.writeto_mem(self.address, 0x24 + row * 24, data)

    def pixel(self, x, y, color=None, blink=None, frame=None):
        """
        Read or write the specified pixel.

        If ``color`` is not specified, returns the current value of the pixel,
        otherwise sets it to the value of ``color``. If ``frame`` is not
        specified, affects the currently active frame. If ``blink`` is
        specified, it enables or disables blinking for that pixel.
        """
        if not 0 <= x <= self.width:
            return
        if not 0 <= y <= self.height:
            return
        if color is None and blink is None:
            return self._register(self._frame, x + y * self.width)
        if frame is None:
            frame = self._frame
        if color is not None:
            if not 0 <= color <= 255:
                raise ValueError("Color out of range")
            self._register(frame, x + y * self.width, color)
        if blink is not None:
            addr, bit = divmod(x + y * self.width, 8)
            bits = self._register(frame, _BLINK_OFFSET + addr)
            if blink:
                bits |= 1 << bit
            else:
                bits &= ~(1 << bit)
            self._register(frame, _BLINK_OFFSET + addr, bits)
