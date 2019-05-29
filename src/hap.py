#!/usr/bin/env python

import logging
import signal
import os


from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_AIR_CONDITIONER

from aircon import Aircon
from util import load_state, save_state

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Airconditioner(Accessory):
    """An AC Accessory"""

    category = CATEGORY_AIR_CONDITIONER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.aircon = Aircon()

        service = self.add_preload_service(
            "HeaterCooler",
            chars=[
                "RotationSpeed",
                "On",
                "CoolingThresholdTemperature",
                "HeatingThresholdTemperature",
                "CurrentTemperature",
            ],
        )
        self.char_rotation_speed = service.configure_char(
            "RotationSpeed",
            setter_callback=self.set_fanspeed,
            getter_callback=self.get_fanspeed,
            properties={"minStep": 25},
        )
        self.char_mode = service.configure_char(
            "TargetHeaterCoolerState",
            setter_callback=self.set_mode,
            getter_callback=self.get_mode,
        )

        self.char_current_mode = service.get_characteristic("CurrentHeaterCoolerState")
        self.char_current_mode.set_value(value=0, should_notify=False)

        self.char_on = service.configure_char(
            "On", setter_callback=self.set_power, getter_callback=self.get_power
        )

        self.char_target_temp = service.configure_char(
            "CoolingThresholdTemperature",
            setter_callback=self.set_cool,
            getter_callback=self.get_temp,
            properties={"minValue": 18, "maxValue": 24, "stepValue": 1},
        )

        self.char_target_temp = service.configure_char(
            "HeatingThresholdTemperature",
            setter_callback=self.set_heat,
            getter_callback=self.get_temp,
            properties={"minValue": 18, "maxValue": 24, "stepValue": 1},
        )

        self.char_current_temp = service.get_characteristic("CurrentTemperature")
        self.char_current_temp.set_value(value=self.aircon.temp, should_notify=False)

    def set_power(self, value):
        print("!!! POWER", value)
        self.aircon.power = value

    def get_power(self):
        return self.aircon.power

    def set_mode(self, value):
        print("!!! MODE", value)
        self.aircon.mode = value
        self.char_current_mode.set_value(value=self.aircon.mode, should_notify=False)

    def get_mode(self):
        return self.aircon.mode

    def set_heat(self, value):
        self.char_current_mode.set_value(value=1, should_notify=False)
        self.char_current_temp.set_value(value=self.aircon.temp, should_notify=False)
        self.aircon.temp = value

    def set_cool(self, value):
        self.char_current_mode.set_value(value=0, should_notify=False)
        self.char_current_temp.set_value(value=self.aircon.temp, should_notify=False)
        self.aircon.temp = value

    def get_temp(self):
        return self.aircon.temp

    def set_fanspeed(self, value):
        print("!!! FANSPEED", value)
        self.aircon.speed = value

    def get_fanspeed(self):
        return self.aircon.speed


# Start the accessory on port 51826
driver = AccessoryDriver(port=51826)
display_name = os.environ.get("DISPLAY_NAME", "Air Conditioner")
accessory = Airconditioner(display_name=display_name, driver=driver)
driver.add_accessory(accessory=accessory)

signal.signal(signal.SIGINT, driver.signal_handler)
signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()
