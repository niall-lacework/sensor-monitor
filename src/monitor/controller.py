from monitor.sensors import AbstractSensor


class Controller:
    def __init__(self):
        self.sensors: list[AbstractSensor] = []

    def add_sensor(self, sensor: AbstractSensor):
        self.sensors.append(sensor)
