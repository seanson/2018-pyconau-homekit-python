#!/usr/bin/env python

import logging
from os import environ
from subprocess import check_output
from time import sleep

logger = logging.getLogger(__name__)


def build_command(*args):
    return '-'.join((str(arg) for arg in args)) + 'C'


MODES = ['off', 'cool', 'heat', 'fan']
SPEEDS = ['quiet', 'low', 'medium', 'high']


class Aircon:
    history = []
    temp = '23'
    mode = 'off'
    speed = 'medium'

    def __init__(self):
        pass

    def _send(self, action):
        command = [
            'irsend',
            'send_once',
            'fujitsu_heat_ac',
            action,
        ]
        logger.info('Sending action: {}'.format(action))
        if 'MOCK_IRSEND' in environ:
            return
        logger.info(check_output(command))

    def turn_on(self):
        if self.mode != 'off':
            return
        self._send('cool-on')
        self.mode = 'cool'
        sleep(1)
        command = build_command(self.mode, self.speed, self.temp)
        return self._send(command)

    def turn_off(self):
        self._send('turn-off')
        self.mode = 'off'

    def set_state(self, mode, speed, temp):
        temp = int(temp)
        if temp > 30:
            raise ValueError('Temperature cannot be above 30')
        if temp < 18:
            raise ValueError('Temperature cannot be below 18')
        if mode not in MODES:
            raise ValueError('Mode {} not found in modes: {}'.format(mode, MODES))
        if speed not in SPEEDS:
            raise ValueError('Speed {} not found in speeds: {}'.format(speed, SPEEDS))
        command = build_command(mode, speed, temp)
        self._send(command)

    def set_speed(self, speed):
        if self.mode == 'off':
            return
        if speed not in SPEEDS:
            raise ValueError('Speed {} not found in speeds: {}'.format(speed, SPEEDS))
        command = build_command(self.mode, speed, self.temp)
        self._send(command)
