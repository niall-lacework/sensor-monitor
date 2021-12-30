from datetime import datetime
import time

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
        self.sensor_id = sensor_id
        self._polling_interval = 1.0
        self._measurement_delay = 0.5

    def get_measurement(self):
        time.sleep(self.measurement_delay)
        return Measurement(self.sensor_id, static_timestamp(), 1.0)

    @property
    def type(self):
        return SensorType.TEMPERATURE


class FakeHumiditySensor(AbstractSensor):
    def __init__(self, sensor_id) -> None:
        self.sensor_id = sensor_id
        self._polling_interval = 1.0
        self._measurement_delay = 0.5

    def get_measurement(self):
        time.sleep(self.measurement_delay)
        return Measurement(self.sensor_id, static_timestamp(), 1.0)

    @property
    def type(self):
        return SensorType.HUMIDITY


@pytest.fixture
def temperature_sensor_fixture():
    yield FakeTemperatureSensor


@pytest.fixture
def humidity_sensor_fixture():
    yield FakeHumiditySensor
