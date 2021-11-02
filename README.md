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

## Operating System

I used the RaspbianPi lite image. You'll need a few extras:

`apt-get install lirc python3-pip`

`pip3 install pyenv`

## Configuring LIRCd

Once you've sorted out which GPIO pins on the RasPi you want to use, these need to be configured in a few locations:

`/boot/config.txt`:

Older kernels (Raspbian Stretch):

`dtoverlay=lirc-rpi,gpio_in_pin=23,gpio_out_pin=22`

Newer kernels (Raspbian Buster):

```
dtoverlay=gpio-ir,gpio_pin=23
dtoverlay=gpio-ir-tx,gpio_pin=22
```

`/etc/lirc/lirc_options.conf`:

Change

`driver = devinput`

to

`driver = default`

You'll also need some sort of configuration for LIRCd to talk to your remote. I managed to find a handy set of configuration for my Fujitsu remote here: [mattjm/Fujitsu_IR](https://github.com/mattjm/Fujitsu_IR).

If not, you'll need to manually capture your IR commands which is beyond the scope of this document.

## Links

- [HAP-Python](https://github.com/ikalchev/HAP-python): The underlying library to support this automation
- [HomeKit Accessory Docs](https://developer.apple.com/support/homekit-accessory-protocol/)
