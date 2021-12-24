from datetime import datetime

import pytest

from monitor.measurements import Measurement
from monitor.sensors import AbstractSensor, SensorType


now = datetime.now()

def static_timestamp():
    return datetime.timestamp(now)

@pytest.fixture
def timestamp_fixture():
    yield static_timestamp()

@pytest.fixture(autouse=True)
def mock_time_stamp(monkeypatch):
    monkeypatch.setattr('monitor.sensors.get_timestamp_now', static_timestamp)

class FakeTemperatureSensor(AbstractSensor):
    def __init__(self, sensor_id) -> None:
        self.senor_id = sensor_id
        self.type = SensorType.TEMPERATURE

    def get_measurement(self):
        return Measurement(self.senor_id, static_timestamp(), 1.0)

class FakeHumiditySensor(AbstractSensor):
    def __init__(self, sensor_id) -> None:
        self.senor_id = sensor_id
        self.type = SensorType.HUMIDITY

    def get_measurement(self):
        return Measurement(self.senor_id, static_timestamp(), 1.0)

@pytest.fixture
def temperature_sensor_fixture():
    yield FakeTemperatureSensor

@pytest.fixture
def humidity_sensor_fixture():
    yield FakeHumiditySensor