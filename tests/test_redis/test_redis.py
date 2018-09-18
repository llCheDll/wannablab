from integrations.redis import RedisClient
from pytest_redis import factories
from config import settings

redis_my_proc = factories.redis_proc(
                    executable='/usr/local/bin/redis-server',
                    host=settings.redis.host,
                    port=settings.redis.port,
                    logsdir='/tmp'
)

redis_my = factories.redisdb('redis_my_proc')


def test_redis_set(redis_my_proc, redis_my):
    redisclient = RedisClient()
    redisclient1 = RedisClient()

    assert redisclient.set('key1', 'value1') is True
    assert redisclient.set('key2', 'value2') is True
    assert redisclient1.set('key3', 'value3') is True
    assert redisclient1.set('key4', 'value4') is True

    values = ['value1', 'value2', 'value3', 'value4']

    assert redisclient.get_multiple('key1', 'key2', 'key3', 'key4') == values

    redis_my.flushall()


def test_redis_getset(redis_my_proc, redis_my):
    redisclient = RedisClient()

    assert redisclient.set('key1', 'value1') is True
    assert redisclient.getset('key1', 'value2') == 'value1'
    assert redisclient.getset('key1', 'value3') == 'value2'

    redis_my.flushall()


def test_redis_hmset(redis_my_proc, redis_my):
    redisclient = RedisClient()

    assert redisclient.hmset('hash_set', key1='value1', key2='value2') is True
    assert redisclient.hmget('hash_set', 'key1', 'key2')[0] == ['value1', 'value2']
    redis_my.flushall()


def test_redis_zset(redis_my_proc, redis_my):
    redisclient = RedisClient()

    assert redisclient.zset('sorted_set', 42, 'key1', 49, 'key2') == 2
    assert redisclient.zrange(
                    'sorted_set', 0, -1
                    ) == [['key1', 'key2']]
    assert redisclient.zrange(
                    'sorted_set', 0, -1, withscores=True
                    )[0] == [('key1', 42), ('key2', 49)]

    redis_my.flushall()

def test_close(redis_my_proc, redis_my):
    redisclient = RedisClient()

    assert redisclient.set('key1', 'value1') is True
    redisclient.close()
    assert redisclient.set('key1', 'value1') is True
