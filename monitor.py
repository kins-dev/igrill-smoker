import os
import json
import time
import mac_config
import logging
import argparse

from igrill import IGrillPeripheral
from utils import setup_log

DATA_FILE = '/tmp/igrill.json'
INTERVAL = 20

def main():

    parser = argparse.ArgumentParser(
        description='Connects to iGrill device and calls a script to process results')
    parser.add_argument(
        '--test',
        dest='test_mode',
        help='Test mode, do not run data.sh',
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
        default='INFO',
        help='Set log level, default: \'info\'')
    parser.add_argument(
        '-d',
        '--log-destination',
        action='store',
        dest='log_destination',
        default='',
        help='Set log destination (file), default: \'\' (stdout)')
    options = parser.parse_args()

    setup_log(options.log_level, options.log_destination)

    if (True = use_mini):
        periph = IGrillMiniPeripheral(mac_config.ADDRESS)
    else:
        periph = IGrillPeripheral(mac_config.ADDRESS)

    try:
        while True:
            if (int(time.time()) % INTERVAL) == 0:
                sensor_data = {
                    'temperature': periph.ReadTemperature(),
                    'battery': periph.ReadBattery(),
                }
                if (True == options.test_mode):
                    logging.debug("Skipping data.sh call")
                else:
                    os.system("./data.sh " + str(sensor_data['battery']) + ' ' + str(sensor_data['temperature'][1]) + ' ' + str(sensor_data['temperature'][4]))

                logging.info('Writing sensor data: {}'.format(sensor_data))
                with open(DATA_FILE, 'w') as f:
                    f.write(json.dumps(sensor_data))
            else:
                time.sleep(0.5)
    except KeyboardInterrupt:
        logging.info("exiting")
    
if __name__ == '__main__':
    main()
