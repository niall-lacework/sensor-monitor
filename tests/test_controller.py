from monitor.controller import Controller


def test_can_add_sensors(temperature_sensor_fixture, humidity_sensor_fixture):
    sensor = temperature_sensor_fixture('sensor_id_1')
    sensor2 = humidity_sensor_fixture('sensor_id_2')
    c = Controller()
    c.add_sensor(sensor)
    c.add_sensor(sensor2)
    assert c.sensors[0] == sensor
    assert c.sensors[1] == sensor2


def test_can_remove_sensors(temperature_sensor_fixture, humidity_sensor_fixture):
    sensor1 = temperature_sensor_fixture('sensor_id_1')
    sensor2 = humidity_sensor_fixture('sensor_id_2')
    c = Controller()
    c.add_sensor(sensor1)
    c.add_sensor(sensor2)
    c.remove_sensor(sensor1)
    assert c.sensors[0] == sensor2
    assert len(c.sensors) == 1


def test_should_not_throw_exception_removing_sensor_that_does_not_exist(temperature_sensor_fixture):
    sensor1 = temperature_sensor_fixture('sensor_id_1')
    c = Controller()
    c.remove_sensor(sensor1)
