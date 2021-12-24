import time

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
    time.sleep(2)
    c.stop_polling()
    assert len(c.get_measurements()) == 2

    sensor_ids = [m.sensor_id for m in c.get_measurements()]
    assert 'sensor_id_1' in sensor_ids
    assert 'sensor_id_2' in sensor_ids
