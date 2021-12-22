from monitor.model import Measurement


def test_measurement_init():
    m = Measurement('sensor_id', 'timestamp', 1.0)
    assert m.sensor_id == 'sensor_id'
    assert m.timestamp == 'timestamp'
    assert m.value == 1.0
