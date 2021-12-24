from monitor.measurements import Measurement


def test_measurement_init(timestamp_fixture):
    m = Measurement('sensor_id', timestamp_fixture, 1.0)
    assert m.sensor_id == 'sensor_id'
    assert m.timestamp == timestamp_fixture
    assert m.value == 1.0


def test_measurement_eq(timestamp_fixture):
    m1 = Measurement('sensor_id', timestamp_fixture, 1.0)
    m2 = Measurement('sensor_id', timestamp_fixture, 1.0)
    assert m1 == m2


def test_measurement_ne(timestamp_fixture):
    m1 = Measurement('sensor_id', timestamp_fixture, 1.0)
    m2 = Measurement('sensor_id', timestamp_fixture, 2.0)
    assert m1 != m2
