import logging
import json

from os import environ
from subprocess import check_output
from time import sleep

from util import load_state, save_state

logger = logging.getLogger(__name__)

SPEEDS = ["off", "quiet", "low", "medium", "high"]
MODES = ["auto", "heat", "cool"]
STEP_VALUE = 100 / len(SPEEDS)


def get_speed_name(value):
    # Values are clamped to 20 so we just cover the ranges
    index = int(value / STEP_VALUE) - 1
    return SPEEDS[index]


def get_mode_name(value):
    return MODES[value]


class Aircon:
    """ A class for managing the Airconditioner state and associated
    LIRC commands """

    MODES = ["off", "cool", "heat", "fan"]

    def __init__(self):
        self.state = load_state()

    def _update(self, action=None):
        """ Build and send a LIRC action through check_output.
        Supports the environment variable MOCK_IRSEND for testing."""
        speed = get_speed_name(self.speed)
        mode = get_mode_name(self.mode)
        if action is "auto":
            logger.warning("Auto mode not supported")
            return
        if action is None:
            action = "{mode}-{speed}-{temp}C".format(
                mode=mode, speed=speed, temp=int(self.temp)
            )

        command = ["irsend", "send_once", "fujitsu_heat_ac", action]
        logger.info("Sending action: {}".format(action))
        if "MOCK_IRSEND" in environ:
            return
        try:
            logger.info(check_output(command))
        except Exception as e:
            logger.warning("Failed to run command: %s - %s", command, e)
        save_state(self.state)
        sleep(0.250)

    @property
    def power(self):
        return self.state["power"]

    @power.setter
    def power(self, value):
        self.state["power"] = value
        if value:
            self._update("{mode}-on".format(mode=get_mode_name(self.mode)))
            self._update()
            return
        self._update("turn-off")

    @property
    def mode(self):
        return self.state["mode"]

    @mode.setter
    def mode(self, value):
        print(value, self.power)
        self.state["mode"] = value
        if self.power:
            if value == "off":
                self.power = False
                return
            self._update()
            return
        self.power = True
        self._update()

    @property
    def temp(self):
        return self.state["temp"]

    @temp.setter
    def temp(self, value):
        self.state["temp"] = value
        save_state(self.state)
        self._update()

    @property
    def room_temp(self):
        return self.state["room_temp"]

    @temp.setter
    def room_temp(self, value):
        self.state["room_temp"] = value
        save_state(self.state)
        self._update()

    @property
    def speed(self):
        return self.state["speed"]

    @speed.setter
    def speed(self, value):
        self.state["speed"] = value
        save_state(self.state)
        self._update()
