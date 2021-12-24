from threading import Thread
import time

from monitor.measurements import Measurement
from monitor.sensors import AbstractSensor


class Controller:
    def __init__(self):
        self.sensors: list[AbstractSensor] = []
        self.stop = False
        self.polling_thread = None

    def add_sensor(self, sensor: AbstractSensor):
        self.sensors.append(sensor)

    def get_measurements(self) -> list[Measurement]:
        measurements: list[Measurement] = [sensor.get_measurement() for sensor in self.sensors]
        return measurements

    def start_polling(self):
        self.stop = False
        self.polling_thread = Thread(target=self.poll_sensors)
        self.polling_thread.start()

    def poll_sensors(self):
        while True and not self.stop:
            self.get_measurements()
            time.sleep(2)

    def stop_polling(self):
        self.stop = True
        if self.polling_thread is not None:
            self.polling_thread.join()
            self.polling_thread = None
