#!/usr/bin/env python

import logging
import signal

from pyhap.accessory import Accessory
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import CATEGORY_THERMOSTAT

from aircon import Aircon

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Airconditioner(Accessory):
    """An AC Accessory"""
    speed = 0
    temperature = 23
    power = False
    category = CATEGORY_THERMOSTAT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aircon = Aircon()

        # Set up fan service to control on/off/speed
        service_fan = self.add_preload_service(
            "Fan", chars=['RotationSpeed', 'On'])

        self.char_rotation_speed = service_fan.configure_char('RotationSpeed',
                                                              setter_callback=self.set_fanspeed,
                                                              getter_callback=self.get_fanspeed)
        self.char_on = service_fan.configure_char('On',
                                                  setter_callback=self.toggle_power,
                                                  getter_callback=self.get_power)

        # Set up target temperature service and default value
        service_temperature = self.add_preload_service("Thermostat")

        self.char_target_temp = service_temperature.configure_char('TargetTemperature',
                                                                   setter_callback=self.set_temp,
                                                                   getter_callback=self.get_temp)

        self.char_current_temp = service_temperature.get_characteristic(
            'CurrentTemperature')
        self.char_current_temp.set_value(
            value=self.temperature, should_notify=False)

    def toggle_power(self, value):
        if value:
            self.aircon.turn_on()
            self.power = True
        else:
            self.aircon.turn_off()
            self.power = False

    def get_power(self):
        return self.power

    def set_temp(self, value):
        self.char_current_temp.set_value(value=value, should_notify=True)
        self.temperature = value

    def get_temp(self):
        return self.temperature

    def set_fanspeed(self, value):
        if value >= 75:
            speed = 'high'
        elif value >= 50:
            speed = 'medium'
        elif value >= 25:
            speed = 'low'
        else:
            speed = 'quiet'
        self.speed = value
        self.aircon.set_speed(speed)

    def get_fanspeed(self):
        return self.speed


# Start the accessory on port 51826
driver = AccessoryDriver(port=51826)
accessory = Airconditioner(display_name="Airconditioner", driver=driver)
driver.add_accessory(accessory=accessory)

signal.signal(signal.SIGINT, driver.signal_handler)
signal.signal(signal.SIGTERM, driver.signal_handler)
driver.start()
