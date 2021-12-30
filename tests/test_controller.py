import time

from monitor.controller import Controller
from monitor.repository import AbstractRepository


class FakeRepo(AbstractRepository):
    def __init__(self) -> None:
        self.measurements = []

    def add_measurement(self, measurement):
        self.measurements.append(measurement)

    def get_measurements(self, sensor_id):
        return [measurement for measurement in self.measurements if measurement.sensor_id == sensor_id]


def test_can_add_sensors(temperature_sensor_fixture, humidity_sensor_fixture):
    sensor = temperature_sensor_fixture('sensor_id_1')
    sensor2 = humidity_sensor_fixture('sensor_id_2')
    c = Controller(FakeRepo())
    c.add_sensor(sensor)
    c.add_sensor(sensor2)
    assert c.sensors[0] == sensor
    assert c.sensors[1] == sensor2


def test_can_remove_sensors(temperature_sensor_fixture, humidity_sensor_fixture):
    sensor1 = temperature_sensor_fixture('sensor_id_1')
    sensor2 = humidity_sensor_fixture('sensor_id_2')
    c = Controller(FakeRepo())
    c.add_sensor(sensor1)
    c.add_sensor(sensor2)
    c.remove_sensor(sensor1)
    assert c.sensors[0] == sensor2
    assert len(c.sensors) == 1


def test_should_not_throw_exception_removing_sensor_that_does_not_exist(temperature_sensor_fixture):
    sensor1 = temperature_sensor_fixture('sensor_id_1')
    c = Controller(FakeRepo())
    c.remove_sensor(sensor1)


def test_can_poll_sensor(temperature_sensor_fixture, timestamp_fixture):
    sensor = temperature_sensor_fixture('sensor_id_1')
    repo = FakeRepo()
    c = Controller(repo)
    c.add_sensor(sensor)
    c.start_polling(polling_interval=2)
    time.sleep(1)  # time for 1 measurement
    c.stop_polling()

    results = repo.get_measurements(sensor.sensor_id)
    assert len(results) == 1
    assert results[0].sensor_id == sensor.sensor_id
    assert results[0].value == 1.0
    assert results[0].timestamp == timestamp_fixture


def test_can_poll_multiple_sensors(temperature_sensor_fixture, timestamp_fixture):
    sensor1 = temperature_sensor_fixture('sensor_id_1')
    sensor2 = temperature_sensor_fixture('sensor_id_2')
    repo = FakeRepo()
    c = Controller(repo)
    c.add_sensor(sensor1)
    c.add_sensor(sensor2)
    c.start_polling(polling_interval=2)
    time.sleep(1)  # time for 1 measurement for each sensor
    c.stop_polling()

    results = repo.get_measurements(sensor1.sensor_id)
    assert len(results) == 1
    assert results[0].sensor_id == sensor1.sensor_id
    assert results[0].value == 1.0
    assert results[0].timestamp == timestamp_fixture

    results = repo.get_measurements(sensor2.sensor_id)
    assert len(results) == 1
    assert results[0].sensor_id == sensor2.sensor_id
    assert results[0].value == 1.0
    assert results[0].timestamp == timestamp_fixture


def test_should_not_poll_sensor_if_not_added(temperature_sensor_fixture, timestamp_fixture):
    sensor = temperature_sensor_fixture('sensor_id_1')
    repo = FakeRepo()
    c = Controller(repo)
    c.start_polling(polling_interval=2)
    time.sleep(1)  # time for 1 measurement
    c.stop_polling()

    results = repo.get_measurements(sensor.sensor_id)
    assert len(results) == 0


def test_should_not_poll_sensor_if_not_started(temperature_sensor_fixture, timestamp_fixture):
    sensor = temperature_sensor_fixture('sensor_id_1')
    repo = FakeRepo()
    c = Controller(repo)
    c.add_sensor(sensor)
    c.stop_polling()

    results = repo.get_measurements(sensor.sensor_id)
    assert len(results) == 0


def test_can_configure_polling_interval(temperature_sensor_fixture, timestamp_fixture):
    sensor = temperature_sensor_fixture('sensor_id_1')
    repo = FakeRepo()
    c = Controller(repo)
    c.add_sensor(sensor)
    c.start_polling(polling_interval=0.1)
    time.sleep(1)  # time for 10 measurements
    c.stop_polling()

    results = repo.get_measurements(sensor.sensor_id)
    assert len(results) == 10
    assert results[0].sensor_id == sensor.sensor_id
    assert results[0].value == 1.0
    assert results[0].timestamp == timestamp_fixture


def test_polling_interval_includes_time_to_take_measurement(temperature_sensor_fixture, timestamp_fixture):
    '''
    If the polling interval is 1s and the time to take a measurement is 0.5s,
    then the controller should know not to wait 1.5s before taking the next measurement.

    i.e. the real polling interval is polling_interval - time_to_take_measurement
    '''
    sensor = temperature_sensor_fixture('sensor_id_1')
    sensor.measurement_delay = 0.5  # time to take a measurement
    repo = FakeRepo()
    c = Controller(repo)
    c.add_sensor(sensor)
    c.start_polling(polling_interval=1)
    time.sleep(1.1)  # time for 2 measurements
    c.stop_polling()

    results = repo.get_measurements(sensor.sensor_id)
    assert len(results) == 2
