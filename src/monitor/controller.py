from threading import Thread
import time

from monitor.measurements import Measurement
from monitor.sensors import AbstractSensor


class Controller:
    '''
    Controller for sensors.
    '''
    def __init__(self):
        self.sensors: list[AbstractSensor] = []
        self.stop = False
        self.polling_thread = None

        self.measurements = []

    def add_sensor(self, sensor: AbstractSensor):
        '''
        Add a sensor to the list of sensors.
        :param sensor: sensor to add
        '''
        self.sensors.append(sensor)

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
        self.stop = True
        if self.polling_thread is not None:
            self.polling_thread.join()
            self.polling_thread = None
