import os
import json
import time

from igrill import IGrillV2Peripheral
ADDRESS = '11:22:33:44:55:66'
DATA_FILE = '/tmp/igrill.json'
INTERVAL = 20

if __name__ == '__main__':

    periph = IGrillV2Peripheral(ADDRESS)

    while True:

        sensor_data = {
            'temperature': periph.read_temperature(),
            'battery': periph.read_battery(),
        }
        os.system("~pi/data.sh " + str(int(sensor_data['battery'])) + ' ' + str(int(sensor_data['temperature'][1])) + ' ' + str(int(sensor_data['temperature'][4])))

        print 'Writing sensor data: {}'.format(sensor_data)
        with open(DATA_FILE, 'w') as f:
            f.write(json.dumps(sensor_data))

        time.sleep(INTERVAL)

