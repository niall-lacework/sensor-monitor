from abc import ABC, abstractmethod
from enum import Enum, auto

from monitor.measurements import Measurement


class SensorType(Enum):
    TEMPERATURE = auto()


class AbstractSensor(ABC):
    '''
    Abstract base class for sensors.
    '''

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

    def __init__(self, sensor_id: str):
        '''
        Initializes a new DS18B20Sensor.
        '''
        self.sensor_id = sensor_id
        self.type = SensorType.TEMPERATURE

    def get_measurement(self) -> Measurement:
        '''
        Returns the current measurement.
        '''
        return Measurement(self.sensor_id, 'timestamp', 1.0)
