import json

from checks import AgentCheck

DATA_FILE = '/tmp/igrill.json'
CONFIG_PATH = '/home/pi/.datadog-agent/conf.d/igrill.yaml'


class IGrillCheck(AgentCheck):

    def read_sensor_data(self):
        with open(DATA_FILE, 'r') as f:
            data = json.loads(f.read())
        return data

    def check(self, instance):
        data = self.read_sensor_data()
        self.gauge('igrill.sensor.temperature', data['temperature'], tags=['igrill'])
        self.gauge('igrill.battery', data['battery'], tags=['igrill'])


if __name__ == '__main__':
    check, instances = IGrillCheck.from_yaml(CONFIG_PATH)
    for instances in instances:
        print '\nRunning check'
        check.check(instance)
        print 'Metrics: {}'.format(check.get_metrics())
