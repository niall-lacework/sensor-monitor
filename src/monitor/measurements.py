from dataclasses import dataclass


@dataclass
class Measurement:
    '''
    A measurement is a single reading from a sensor.
    '''
    sensor_id: str
    timestamp: float
    value: float
