import sys

from pytest_redis import factories

from monitor.repository import RedisRepository
from monitor.measurements import Measurement

if sys.platform == 'darwin':  # local testing on mac
    redis_my_proc = factories.redis_proc(executable='/usr/local/bin/redis-server', port=None, datadir='/tmp/pytest')
    fake_redis_db = factories.redisdb('redis_my_proc')
else:  # CI testing. Redis is already running on port 6379
    fake_redis_db = factories.redisdb('redis_nooproc')


def test_redis_repository_get_measurements(timestamp_fixture, fake_redis_db):
    measurement = Measurement('sensor_id', timestamp_fixture, 1.0)
    repo = RedisRepository(fake_redis_db)

    repo.add_measurement(measurement)
    assert repo.get_measurements('sensor_id')[0] == measurement


def test_redis_repository_pop_measurements(timestamp_fixture, fake_redis_db):
    measurement1 = Measurement('sensor_id', timestamp_fixture, 1.0)
    measurement2 = Measurement('sensor_id', timestamp_fixture, 2.0)
    repo = RedisRepository(fake_redis_db)

    repo.add_measurement(measurement1)
    repo.add_measurement(measurement2)

    popped1 = repo.pop_measurement()
    assert popped1 == measurement1

    popped2 = repo.pop_measurement()
    assert popped2 == measurement2
