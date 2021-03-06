from pathlib import Path

import pytest

from monitor.sensors import DS18B20Sensor, SensorType, SensorInitError, SensorMeasurementError, SensorConfigError


@pytest.fixture
def good_measurement():
    return '''bd 00 4b 46 ff ff ff ff ff ff : crc=ff YES
    bd 00 4b 46 ff ff ff ff ff ff t=27772'''


def test_ds18b20_init(tmpdir):
    device_file = Path(tmpdir) / 'sensor.txt'
    device_file.touch()
    s = DS18B20Sensor('sensor_id', device_file)
    assert s.sensor_id == 'sensor_id'
    assert s.type == SensorType.TEMPERATURE
    assert s.measurement_delay == 1.0
    assert s.polling_interval == 1.0


def test_ds18b20_init_bad_device_file(tmpdir):
    device_file = Path(tmpdir) / 'sensor.txt'
    with pytest.raises(SensorInitError):
        DS18B20Sensor('sensor_id', device_file)


def test_ds18b20_can_set_polling_interval(tmpdir):
    device_file = Path(tmpdir) / 'sensor.txt'
    device_file.touch()
    s = DS18B20Sensor('sensor_id', device_file)
    s.polling_interval = 2.0
    assert s.polling_interval == 2.0


def test_ds18b20_can_set_measurement_delay(tmpdir):
    device_file = Path(tmpdir) / 'sensor.txt'
    device_file.touch()
    s = DS18B20Sensor('sensor_id', device_file)
    s.measurement_delay = 2.0
    assert s.measurement_delay == 2.0


def test_ds18b20_cannot_set_measurement_delay_less_than_zero(tmpdir):
    device_file = Path(tmpdir) / 'sensor.txt'
    device_file.touch()
    s = DS18B20Sensor('sensor_id', device_file)
    with pytest.raises(SensorConfigError):
        s.measurement_delay = -1.0


def test_ds18b20_should_update_polling_interval_if_measurement_delay_set_to_more_than_polling_interval(tmpdir, good_measurement):
    device_file = Path(tmpdir) / 'sensor.txt'
    device_file.write_text(good_measurement)
    s = DS18B20Sensor('sensor_id', device_file)
    s.measurement_delay = 2.0
    assert s.polling_interval == 2.0


def test_cannot_set_polling_interval_less_than_measurement_delay(tmpdir):
    device_file = Path(tmpdir) / 'sensor.txt'
    device_file.touch()
    s = DS18B20Sensor('sensor_id', device_file)
    with pytest.raises(SensorConfigError):
        s.polling_interval = 0.5


def test_ds18b20_get_measurement(tmpdir, timestamp_fixture, good_measurement):
    device_file = Path(tmpdir) / 'sensor.txt'
    device_file.write_text(good_measurement)
    s = DS18B20Sensor('sensor_id', device_file)
    m = s.get_measurement()
    assert m.sensor_id == 'sensor_id'
    assert m.timestamp == timestamp_fixture
    assert m.value == 27.8


@pytest.fixture
def bad_crc():
    return '''bd 00 4b 46 ff ff ff ff ff ff : crc=ff NO
    bd 00 4b 46 ff ff ff ff ff ff t=27812'''


def test_ds18b20_get_measurement_bad_crc(tmpdir, bad_crc):
    device_file = Path(tmpdir) / 'sensor.txt'
    device_file.write_text(bad_crc)
    s = DS18B20Sensor('sensor_id', device_file)
    with pytest.raises(SensorMeasurementError):
        s.get_measurement()


@pytest.fixture
def missing_t_measurement():
    return '''bd 00 4b 46 ff ff ff ff ff ff : crc=ff YES
    bd 00 4b 46 ff ff ff ff ff ff '''


def test_ds18b20_get_measurement_missing_t_measurement(tmpdir, missing_t_measurement):
    device_file = Path(tmpdir) / 'sensor.txt'
    device_file.write_text(missing_t_measurement)
    s = DS18B20Sensor('sensor_id', device_file)
    with pytest.raises(SensorMeasurementError):
        s.get_measurement()


@pytest.fixture
def not_a_number_measurement():
    return '''bd 00 4b 46 ff ff ff ff ff ff : crc=ff YES
    bd 00 4b 46 ff ff ff ff ff ff t=278a2'''


def test_ds18b20_get_measurement_not_a_number_measurement(tmpdir, not_a_number_measurement):
    device_file = Path(tmpdir) / 'sensor.txt'
    device_file.write_text(not_a_number_measurement)
    s = DS18B20Sensor('sensor_id', device_file)
    with pytest.raises(SensorMeasurementError):
        s.get_measurement()


def test_ds18b20_get_measurement_rounds_to_one_decimal(tmpdir, timestamp_fixture, good_measurement):
    device_file = Path(tmpdir) / 'sensor.txt'
    device_file.write_text(good_measurement)
    s = DS18B20Sensor('sensor_id', device_file)
    m = s.get_measurement()
    assert m.sensor_id == 'sensor_id'
    assert m.timestamp == timestamp_fixture
    assert m.value == 27.8
