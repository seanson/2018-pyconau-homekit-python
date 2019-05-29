import logging
import json

logger = logging.getLogger(__name__)


DEFAULT_STATE = {"mode": 2, "temp": 18, "speed": 40, "power": 0}


def load_state():
    """ Manage state so we can persist HomeKit state between reboots """
    try:
        with open(".state.json", "r") as state_file:
            state = json.load(fp=state_file)
        logging.info("Aircon config loaded.")
    except IOError:
        logging.info("Could not load state cache .state.json, loading defaults.")
        state = DEFAULT_STATE
    logging.info(state)
    return state


def save_state(state):
    try:
        with open(".state.json", "w") as state_file:
            json.dump(obj=state, fp=state_file, indent=2)
        logging.info("Aircon config saved.")
    except IOError as e:
        logging.info("Could not save state cache .state.json: %s", e)
