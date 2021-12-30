import logging

from monitor.sensors import AbstractSensor

LOG = logging.getLogger(__name__)


class Controller:
    '''
    Controller for sensors.
    '''
    def __init__(self):
        self._sensors: list[AbstractSensor] = []

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

    def poll_sensor(self, sensor: AbstractSensor, polling_interval: float):
        '''
        Poll sensors in a separate thread.
        :param polling_interval: polling interval in seconds
        '''
        LOG.info('Polling sensor - [{}] with interval - [{}]'.format(sensor.sensor_id, polling_interval))

    def stop_polling(self):
        '''
        Stop polling sensors.
        '''
        LOG.info('Stopping polling sensors')
