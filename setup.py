from distutils.core import setup


setup(
    name='micropython-adafruit-is31fl3731',
    py_modules=['is31fl3731'],
    version="1.0",
    description="Driver for MicroPython for the IS31FL3731 LED matrix.",
    long_description="""\
Driver for the IS31FL3731-based charlieplexed LED matrices and CharlieWing.""",
    author='Radomir Dopieralski',
    author_email='micropython@sheep.art.pl',
    classifiers = [
        'Development Status :: 6 - Mature',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
