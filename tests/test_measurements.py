from monitor.measurements import Measurement


def test_measurement_init():
    m = Measurement('sensor_id', 'timestamp', 1.0)
    assert m.sensor_id == 'sensor_id'
    assert m.timestamp == 'timestamp'
    assert m.value == 1.0


def test_measurement_eq():
    m1 = Measurement('sensor_id', 'timestamp', 1.0)
    m2 = Measurement('sensor_id', 'timestamp', 1.0)
    assert m1 == m2


def test_measurement_ne():
    m1 = Measurement('sensor_id', 'timestamp', 1.0)
    m2 = Measurement('sensor_id', 'timestamp', 2.0)
    assert m1 != m2
