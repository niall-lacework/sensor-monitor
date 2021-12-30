import logging
from threading import Thread
import time

from monitor.measurements import Measurement
from monitor.sensors import AbstractSensor

LOG = logging.getLogger(__name__)


class Controller:
    '''
    Controller for sensors.
    '''
    def __init__(self):
        self._sensors: list[AbstractSensor] = []
        self.stop = False
        self.polling_thread = None

        self.measurements = []

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

    def get_measurements(self) -> list[Measurement]:
        '''
        Returns the current measurements for all sensors.
        :return: list of measurements
        '''
        measurements: list[Measurement] = [sensor.get_measurement() for sensor in self.sensors]
        return measurements

    def start_polling(self, polling_interval: float = 2):
        '''
        Start polling sensors in a separate thread.
        :param polling_interval: polling interval in seconds
        '''
        LOG.info('Starting polling sensors with interval - [{}]'.format(polling_interval))
        if polling_interval <= 0:
            raise ValueError('Polling interval must be a positive number')
        self.stop = False
        self.polling_thread = Thread(target=self.poll_sensors, args=(polling_interval,))
        self.polling_thread.start()

    def poll_sensors(self, polling_interval: float):
        '''
        Poll sensors in a separate thread.
        :param polling_interval: polling interval in seconds
        '''
        while True and not self.stop:
            self.measurements.extend(self.get_measurements())
            time.sleep(polling_interval)

    def stop_polling(self):
        '''
        Stop polling sensors.
        '''
        LOG.info('Stopping polling sensors')
        self.stop = True
        if self.polling_thread is not None:
            self.polling_thread.join()
            self.polling_thread = None
