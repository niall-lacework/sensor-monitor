from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto
from pathlib import Path

from monitor.measurements import Measurement


class SensorInitError(Exception):
    '''
    Exception for sensor initialisation errors.
    '''
    pass


class SensorMeasurementError(Exception):
    '''
    Exception for sensor measurement errors.
    '''
    pass


class SensorType(Enum):
    TEMPERATURE = auto()
    HUMIDITY = auto()


class AbstractSensor(ABC):
    '''
    Abstract base class for sensors.
    '''

    type: SensorType = None  # type: ignore
    
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id: str = sensor_id

    @abstractmethod
    def get_measurement(self) -> Measurement:
        '''
        Returns the current measurement.
        '''
        pass


class DS18B20Sensor(AbstractSensor):
    '''
    A sensor that measures the temperature of a DS18B20 sensor.
    '''

    type = SensorType.TEMPERATURE

    def __init__(self, sensor_id: str, device_file: Path):
        '''
        Initializes a new DS18B20Sensor.

        :param sensor_id: sensor id
        :param device_file: path to the device file

        '''
        self.sensor_id = sensor_id
        self.device_file = device_file

        if not device_file.is_file():
            raise SensorInitError('Device file does not exist')

    def _read_device_file(self):
        with open(self.device_file, 'r') as f:
            lines = f.readlines()
        return lines

    def get_measurement(self) -> Measurement:
        '''
        Returns the current measurement.

        :return: a measurement
        raises: SensorMeasurementError
        '''
        raw_measurement = self._read_device_file()
        if raw_measurement[0].strip()[-3:] != 'YES':  # check CRC
            raise SensorMeasurementError(
                'Error reading sensor [{}] from device file [{}] bad CRC'.format(self.sensor_id, self.device_file)
                )

        equals_pos = raw_measurement[1].find('t=')  # find temperature
        if equals_pos == -1:
            raise SensorMeasurementError(
                'Error reading sensor [{}] from device file [{}] cannot determine temperature value'.format(self.sensor_id, self.device_file)
                )

        temp_string = raw_measurement[1][equals_pos+2:]

        try:
            temp_c = round(float(temp_string) / 1000.0, 1)  # convert to celsius
        except ValueError:
            raise SensorMeasurementError(
                'Error reading sensor [{}] from device file [{}] cannot convert [{}] to celcius'.format(self.sensor_id, self.device_file, temp_string)
                )

        return Measurement(self.sensor_id, get_timestamp_now(), temp_c)


def get_timestamp_now() -> float:
    '''
    Returns the current timestamp.
    '''
    return datetime.timestamp(datetime.now())
