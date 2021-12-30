import logging
from threading import Thread
import time

from monitor.sensors import AbstractSensor
from monitor.repository import AbstractRepository

LOG = logging.getLogger('monitor_logger')


class Controller:
    '''
    Controller for sensors.
    '''
    def __init__(self, repo: AbstractRepository):
        self.repo = repo

        self._sensors: list[AbstractSensor] = []
        self._polling_threads: list[Thread] = []

    @property
    def sensors(self):
        return self._sensors

    def add_sensor(self, sensor: AbstractSensor):
        '''
        Add a sensor to the list of sensors.
        :param sensor: sensor to add
        '''
        self._sensors.append(sensor)
        LOG.info('Added sensor - [{}]'.format(sensor.sensor_id))

    def remove_sensor(self, sensor: AbstractSensor):
        '''
        Remove a sensor from the list of sensors.
        :param sensor: sensor to remove
        '''
        try:
            self._sensors.remove(sensor)
            LOG.info('Removed sensor - [{}]'.format(sensor.sensor_id))
        except ValueError:
            LOG.error('Sensor not found - [{}]'.format(sensor.sensor_id))

    def start_polling(self, polling_interval: float = 2):
        '''
        Start polling sensors in a separate thread.
        :param polling_interval: polling interval in seconds
        '''
        LOG.info('Starting polling sensors with interval - [{}]'.format(polling_interval))
        self.running = True
        for sensor in self._sensors:
            t = Thread(target=self.poll_sensor, args=(sensor,))
            t.start()
            self._polling_threads.append(t)

    def poll_sensor(self, sensor: AbstractSensor):
        '''
        Poll sensors in a separate thread.
        :param polling_interval: polling interval in seconds
        '''
        polling_interval = sensor.polling_interval
        while True and self.running:
            LOG.info('Polling sensor - [{}] with interval - [{}]'.format(sensor.sensor_id, polling_interval))
            start = time.time()
            measurement = sensor.get_measurement()
            stop = time.time()
            self.repo.add_measurement(measurement)
            time.sleep(polling_interval - (stop - start))

    def stop_polling(self):
        '''
        Stop polling sensors.
        '''
        self.running = False
        LOG.info('Stopping polling sensors')
        for t in self._polling_threads:
            t.join()
        self._polling_threads = []
        LOG.info('Polling sensors stopped')
