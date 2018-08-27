# PyConAU 2018

## Automating Your Home with Python, Raspberry Pi and HomeKit

This is the sample code from my talk from my 2018 PyConAU IoT track talk in Sydney.

[Talk Page](https://2018.pycon-au.org/talks/45170-automating-your-home-with-python-raspberry-pi-and-homekit/)

[![Automating Your Home with Python, Raspberry Pi and HomeKit](https://img.youtube.com/vi/SiLtPgeTZLA/0.jpg)](https://www.youtube.com/watch?v=SiLtPgeTZLA)

[Youtube Link](https://www.youtube.com/watch?v=SiLtPgeTZLA)

## Contents

- `src/hap.py`: The main script for initialising a HomeKit Accessory
- `src/aircon.py`: A wrapper script around `irsend` for sending IR commands via LIRC
- `slides.pdf`: A pdf export of the original slides used.

## Usage

Pip or pipenv can be used to install the requirements.

Run `python src/hap.py` to start the sample or `MOCK_IRSEND=true python src/hap.py` to mock the irsend commands for testing.

## Links

- [HAP-Python](https://github.com/ikalchev/HAP-python): The underlying library to support this automation
- [HomeKit Accessory Docs](https://developer.apple.com/support/homekit-accessory-protocol/)
- [LIRC on RasPi Setup](https://gist.github.com/prasanthj/c15a5298eb682bde34961c322c95378b)
