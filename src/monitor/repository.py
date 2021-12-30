from abc import ABC, abstractmethod
from dataclasses import asdict
import json

from monitor.measurements import Measurement
from redis import Redis  # type: ignore


class AbstractRepository(ABC):
    '''
    Abstract base class for repositories.
    '''

    @abstractmethod
    def add_measurement(self, measurement: Measurement) -> None:
        '''
        Adds a measurement to the repository.
        '''
        pass


class RedisRepository(AbstractRepository):
    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client

    def add_measurement(self, measurement: Measurement) -> None:
        self.redis_client.rpush('measurements', json.dumps(asdict(measurement)))

    def get_measurements(self, sensor_id: str) -> list[Measurement]:
        all_measurements = self.redis_client.lrange('measurements', 0, -1)
        measurements = [Measurement(**json.loads(measurement)) for measurement in all_measurements]
        return [measurement for measurement in measurements if measurement.sensor_id == sensor_id]

    def pop_measurement(self) -> Measurement:
        measurement = self.redis_client.lpop('measurements')
        return Measurement(**json.loads(measurement))
