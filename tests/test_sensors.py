from monitor.sensors import DS18B20Sensor, SensorType


def test_ds18b20_sensor_init():
    s = DS18B20Sensor('sensor_id')
    assert s.sensor_id == 'sensor_id'
    assert s.type == SensorType.TEMPERATURE


def test_ds18b20_sensor_get_measurement():
    s = DS18B20Sensor('sensor_id')
    m = s.get_measurement()
    assert m.sensor_id == 'sensor_id'
    assert m.timestamp == 'timestamp'
    assert m.value == 1.0
