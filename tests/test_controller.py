import time

import pytest

from monitor.controller import Controller


def test_can_add_sensors(temperature_sensor_fixture, humidity_sensor_fixture):
    sensor = temperature_sensor_fixture('sensor_id_1')
    sensor2 = humidity_sensor_fixture('sensor_id_2')
    c = Controller()
    c.add_sensor(sensor)
    c.add_sensor(sensor2)
    assert c.sensors[0] == sensor
    assert c.sensors[1] == sensor2


def test_can_get_measurement(temperature_sensor_fixture, timestamp_fixture):
    sensor = temperature_sensor_fixture('sensor_id')
    c = Controller()
    c.add_sensor(sensor)
    measurements = c.get_measurements()
    assert len(measurements) == 1

    m = measurements[0]
    assert m.sensor_id == 'sensor_id'
    assert m.timestamp == timestamp_fixture
    assert m.value == 1.0


def test_can_get_measurement_with_multiple_sensors(temperature_sensor_fixture, humidity_sensor_fixture, timestamp_fixture):
    sensor1 = temperature_sensor_fixture('sensor_id_1')
    sensor2 = humidity_sensor_fixture('sensor_id_2')
    c = Controller()
    c.add_sensor(sensor1)
    c.add_sensor(sensor2)
    measurements = c.get_measurements()
    assert len(measurements) == 2

    m1 = measurements[0]
    assert m1.sensor_id == 'sensor_id_1'
    assert m1.timestamp == timestamp_fixture
    assert m1.value == 1.0

    m2 = measurements[1]
    assert m2.sensor_id == 'sensor_id_2'
    assert m2.timestamp == timestamp_fixture
    assert m2.value == 1.0


def test_can_poll_sensors(temperature_sensor_fixture, humidity_sensor_fixture):
    sensor1 = temperature_sensor_fixture('sensor_id_1')
    sensor2 = humidity_sensor_fixture('sensor_id_2')
    c = Controller()
    c.add_sensor(sensor1)
    c.add_sensor(sensor2)
    c.start_polling()
    c.stop_polling()
    result = c.measurements
    assert len(result) == 2

    sensor_ids = [m.sensor_id for m in result]
    assert 'sensor_id_1' in sensor_ids
    assert 'sensor_id_2' in sensor_ids


def test_polling_interval_can_be_set(temperature_sensor_fixture):
    sensor1 = temperature_sensor_fixture('sensor_id_1')
    c = Controller()
    c.add_sensor(sensor1)
    c.start_polling(polling_interval=2)
    time.sleep(3)  # wait for 3 seconds. Should be enough time to get 2 measurements
    c.stop_polling()
    result = c.measurements
    assert len(result) == 2

    sensor_ids = [m.sensor_id for m in result]
    assert 'sensor_id_1' in sensor_ids


def test_polling_interval_cannot_be_negative(temperature_sensor_fixture):
    sensor1 = temperature_sensor_fixture('sensor_id_1')
    c = Controller()
    c.add_sensor(sensor1)
    with pytest.raises(ValueError):
        c.start_polling(polling_interval=-1)


def test_polling_sensors_if_sensor_measurement_is_longer_than_polling_interval(temperature_sensor_fixture):
    sensor1 = temperature_sensor_fixture('sensor_id_1')
    sensor1.measurement_delay = 3
    c = Controller()
    c.add_sensor(sensor1)
    c.start_polling(polling_interval=1)
    time.sleep(2)  # wait for 2 seconds. Should be enough time to get 1 measurement
    c.stop_polling()
    result = c.measurements
    assert len(result) == 1

    sensor_ids = [m.sensor_id for m in result]
    assert 'sensor_id_1' in sensor_ids
