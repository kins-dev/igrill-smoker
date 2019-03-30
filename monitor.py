import os
import json
import time
import mac_config

from igrill import IGrillV2Peripheral

DATA_FILE = '/tmp/igrill.json'
INTERVAL = 20

if __name__ == '__main__':

    periph = IGrillV2Peripheral(mac_config.ADDRESS)

    while True:
        if (int(time.time()) % INTERVAL) == 0:
            sensor_data = {
                'temperature': periph.read_temperature(),
                'battery': periph.read_battery(),
            }
            os.system("bash ~/igrill-smoker/data.sh " + str(sensor_data['battery']) + ' ' + str(sensor_data['temperature'][1]) + ' ' + str(sensor_data['temperature'][4]))

            print 'Writing sensor data: {}'.format(sensor_data)
            with open(DATA_FILE, 'w') as f:
                f.write(json.dumps(sensor_data))
        else:
            time.sleep(0.5)

