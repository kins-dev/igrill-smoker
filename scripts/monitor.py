# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
import os
import json
import time
import logging
import argparse
import configparser
import sys

from py_utils.igrill import IGrillPeripheral, IGrillMiniPeripheral
from py_utils.logging import SetupLog
from py_config.mac_config import ADDRESS

# TODO: make this a config variable
DATA_FILE = sys.path[0]+'/../run/igrill.json'

def main():
    config = configparser.ConfigParser()
    # does not throw an error, just returns the empty set if the file doesn't exist
    config.read(sys.path[0]+'/../config/iGrill_config.ini')
    food_probe = config.getint("Probes", "FoodProbe", fallback=1)
    smoke_probe = config.getint("Probes", "SmokeProbe", fallback=4)
    poll_time = config.getint("Reporting", "PollTime", fallback=20)
    loglevel = config.get("Logging", "LogLevel", fallback="INFO")
    logfile = config.get("Logging", "LogFile", fallback="")
    igrill_type = config.get("iGrill", "Type", fallback="Standard")

    parser = argparse.ArgumentParser(
        description='Connects to iGrill device and calls a script to process results')
    parser.add_argument(
        '--test',
        dest='test_mode',
        help='Test mode, do not run data.sh',
        action='store_true')
    parser.add_argument(
        '--once',
        dest='single_shot_mode',
        help='Run now, no wait, only once (implies test mode)',
        action='store_true')
    parser.add_argument(
        '--mini',
        dest='use_mini',
        help='Use an iGrill mini',
        action='store_true')
    parser.add_argument(
        '-l',
        '--log-level',
        action='store',
        dest='log_level',
        default=loglevel,
        help='Set log level, default: \'' + loglevel + '\'')
    parser.add_argument(
        '-d',
        '--log-destination',
        action='store',
        dest='log_destination',
        default=logfile,
        help='Set log destination (file), default: \'' + logfile + '\'')
    options = parser.parse_args()

    SetupLog(options.log_level, options.log_destination)

    if (True == options.use_mini or "mini" == igrill_type):
        peripheral = IGrillMiniPeripheral(ADDRESS)
    else:
        peripheral = IGrillPeripheral(ADDRESS)

    try:
        if (True == options.single_shot_mode):
            sensor_data = {
                'temperature': peripheral.ReadTemperature(),
                'battery': peripheral.ReadBattery(),
            }
            logging.info('Sensor data: {}'.format(sensor_data))
        else:
            while True:
                if (int(time.time()) % poll_time) == 0:
                    sensor_data = {
                        'temperature': peripheral.ReadTemperature(),
                        'battery': peripheral.ReadBattery(),
                    }
                    if (True == options.test_mode):
                        logging.debug("Skipping data.sh call")
                    else:
                        os.system(sys.path[0]+"/data.sh " +
                            str(sensor_data['battery']) + ' ' +
                            str(sensor_data['temperature'][smoke_probe - 1]) + ' ' +
                            str(sensor_data['temperature'][food_probe - 1]))
                    if (True == options.test_mode):
                        logging.info("Skipping sensor data write.  Data: {}".format(sensor_data))
                    else:
                        logging.info('Writing sensor data: {}'.format(sensor_data))
                        with open(DATA_FILE, 'w') as f:
                            f.write(json.dumps(sensor_data))
                else:
                    time.sleep(0.5)
    except KeyboardInterrupt:
        logging.info("exiting")
    
if __name__ == '__main__':
    main()
