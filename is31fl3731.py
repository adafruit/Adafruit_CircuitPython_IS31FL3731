import time


_MODE_REGISTER = _const(0x00)
_FRAME_REGISTER = _const(0x01)
_SHUTDOWN_REGISTER = _const(0x0a)
_AUDIOSYNC_REGISTER = _const(0x06)

_CONFIG_BANK = _const(0x0b)
_BANK_ADDRESS = _const(0xfd)

_PICTURE_MODE = _const(0x00)
_AUTOPLAY_MODE = _const(0x08)
_AUDIOPLAY_MODE = _const(0x18)


class IS31FL3731:
    def __init__(self, width, height, i2c, address=0x74):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.address = address
        self.reset()
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

    def init(self):
        self._mode(_PICTURE_MODE)
        self.frame(0)
        self.fill(0)
        for frame in range(8):
            for col in range(18):
                self._register(frame, col, 0xff)
        self.audio_sync(False)

    def _mode(self, mode=None):
        return self._register(_CONFIG_BANK, _MODE_REGISTER, mode)

    def reset(self):
        self._register(_CONFIG_BANK, _SHUTDOWN_REGISTER, 0x00)
        time.delay_ms(10)
        self._register(_CONFIG_BANK, _SHUTDOWN_REGISTER, 0x01)

    def frame(self, frame=None, show=True):
        if frame is None:
            return self._frame
        if not 0 <= frame <= 8:
            raise ValueError("Frame out of range")
        self._frame = frame
        if show:
            self._register(_CONFIG_BANK, _FRAME_REGISTER, frame);

    def fill(self, color=0, frame=None):
        if not 0 <= color <= 255:
            raise ValueError("Color out of range")
        if frame is None:
            frame = self._frame
        self._bank(frame)
        data = bytearray([color] * 24)
        for row in range(6):
            self.i2c.writeto_mem(self.address, 0x24 + row * 24, data)

    def audio_sync(self, value=None):
        return self._register(_CONFIG_BANK, _AUDIOSYNC_REGISTER, value)

    def pixel(self, x, y, color=None, frame=None):
        if not 0 <= x <= self.width:
            return
        if not 0 <= y <= self.height:
            return
        if color is None:
            return self._register(self._frame, x + y * self.width)
        if not 0 <= color <= 255:
            raise ValueError("Color out of range")
        if frame is None:
            frame = self._frame
        self._register(frame, x + y * self.width, color)
