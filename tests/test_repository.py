import sys

from pytest_redis import factories

from monitor.repository import RedisRepository
from monitor.measurements import Measurement

if sys.platform == 'darwin':
    executable = '/usr/local/bin/redis-server'
else:
    executable = '/usr/bin/redis-server'

redis_my_proc = factories.redis_proc(executable=executable, port=None, datadir='/tmp/pytest')
fake_redis_db = factories.redisdb('redis_my_proc')


def test_redis_repository(timestamp_fixture, fake_redis_db):
    measurement = Measurement('sensor_id', timestamp_fixture, 1.0)
    repo = RedisRepository(fake_redis_db)

    repo.add_measurement(measurement)
    assert repo.get_measurements('sensor_id')[0] == measurement
