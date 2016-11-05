import json
import time

from igrill import IGrillMiniPeripheral

ADDRESS = 'D4:81:CA:05:53:5E'
DATA_FILE = '/tmp/igrill.json'
INTERVAL = 15

if __name__ == '__main__':

    periph = IGrillMiniPeripheral(ADDRESS)

    while True:

        sensor_data = {
            'temperature': periph.read_temperature(),
            'battery': periph.read_battery(),
        }

        print 'Writing sensor data: {}'.format(sensor_data)
        with open(DATA_FILE, 'w') as f:
            f.write(json.dumps(sensor_data))

        time.sleep(INTERVAL)

