from monitor.measurements import Measurement
from monitor.sensors import AbstractSensor, SensorType
from monitor.controller import Controller


class FakeSensor(AbstractSensor):
    def __init__(self, sensor_id) -> None:
        self.senor_id = sensor_id
        self.type = SensorType.TEMPERATURE

    def get_measurement(self):
        return Measurement(self.senor_id, 'timestamp', 1.0)


def test_can_add_sensors():
    sensor = FakeSensor('sensor_id')
    c = Controller()
    c.add_sensor(sensor)
    assert c.sensors[0] == sensor
