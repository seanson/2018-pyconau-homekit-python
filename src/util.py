import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


DEFAULT_STATE = {"mode": 2, "temp": 18, "speed": 40, "power": 0}
METRICS_PATH = Path('/var/lib/prometheus/node-exporter')

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


def save_state(state, metrics=True):
    try:
        with open(".state.json", "w") as state_file:
            json.dump(obj=state, fp=state_file, indent=2)
        logging.info("Aircon config saved.")
    except IOError as e:
        logging.info("Could not save state cache .state.json: %s", e)
    if not metrics:
      return
    if not METRICS_PATH.exists():
      logging.warn(f"Metrics enabled but {METRICS_PATH} does not exist")
      return
    metrics = f"""
# HELP homekit_fan_speed The speed of the air conditioner fan
# TYPE homekit_fan_speed gauge
homekit_fan_speed {state['speed']}
# HELP homekit_temperature_celcius The temperature of the air conditioner
# TYPE homekit_temperature_celcius gauge
homekit_temperature_celcius {state['temp']}
# HELP homekit_power_state The power state of the air conditioner
# TYPE homekit_power_state gauge
homekit_power_state {"1" if state['power'] else "0"}
"""
    with open(METRICS_PATH / "python-homekit.prom", "w") as metrics_file:
      metrics_file.write(metrics)


