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


def test_redis_keys(redis_my):
    redisclient = RedisClient()

    assert redisclient.set('key1', 'value1') is True
    assert redisclient.set('key2', 'value2') is True
    assert redisclient.set('key3', 'value3') is True
    assert redisclient.set('key4', 'value4') is True

    assert redisclient.keys('*3*') == ['key3']
    assert redisclient.keys('ke?3') == ['key3']
    assert redisclient.keys('k*y2') == ['key2']
    assert redisclient.keys('ke[ye]1') == ['key1']
    assert redisclient.keys('ke[^e]4') == ['key4']
    assert redisclient.keys('[j-o]ey1') == ['key1']

    redis_my.flushall()


def test_redis_zcard(redis_my):
    redisclient = RedisClient()

    redisclient.zset('sorted_set', 42, 'key1', 49, 'key2', 1, 'key3')
    redisclient.zset('sorted_set', 50, 'key4', 13, 'key5')

    assert redisclient.zcard('sorted_set') == 5

    redis_my.flushall()


def test_redis_zrank(redis_my):
    redisclient = RedisClient()

    redisclient.zset('sorted_set', 42, 'key1', 49, 'key2', 1, 'key3')

    assert redisclient.zrank('sorted_set', 'key2') == 2
    assert redisclient.zrank('sorted_set', 'key1') == 1
    assert redisclient.zrank('sorted_set', 'key3') == 0

    redis_my.flushall()


def test_redis_close(redis_my):
    redisclient = RedisClient()

    assert redisclient.set('key1', 'value1') is True
    assert redisclient.get('key1') == 'value1'

    redisclient.close()

    try:
        assert redisclient.get('key1') == 'value1'
    except AttributeError as e:
        assert str(e) == "\'RedisClient\' object has no attribute \'_connection\'"

    redis_my.flushall()


def test_redis_set(redis_my):
    redisclient = RedisClient()

    assert redisclient.set('key1', 'value1') is True
    assert redisclient.set('key2', 'value2') is True
    assert redisclient.set('key3', 'value3') is True
    assert redisclient.set('key4', 'value4') is True

    values = ['value1', 'value2', 'value3', 'value4']

    assert redisclient.get_multiple('key1', 'key2', 'key3', 'key4') == values

    redis_my.flushall()


def test_redis_get(redis_my):
    redisclient = RedisClient()

    assert redisclient.set('key1', 'value1') is True

    assert redisclient.get('key1') == 'value1'
    assert redisclient.get('key2') is None

    redis_my.flushall()


def test_redis_getset(redis_my):
    redisclient = RedisClient()

    assert redisclient.set('key1', 'value1') is True
    assert redisclient.getset('key1', 'value2') == 'value1'
    assert redisclient.getset('key1', 'value3') == 'value2'

    redis_my.flushall()


def test_redis_hmset(redis_my):
    redisclient = RedisClient()

    assert redisclient.hmset('hash_set', key1='value1', key2='value2') is True
    assert redisclient.hmget('hash_set', 'key1', 'key2')[0] == ['value1', 'value2']
    redis_my.flushall()


def test_redis_zset(redis_my):
    redisclient = RedisClient()

    assert redisclient.zset('sorted_set', 42, 'key1', 49, 'key2') == 2
    assert redisclient.zrange(
                    'sorted_set', 0, -1
                    ) == [['key1', 'key2']]
    assert redisclient.zrange(
                    'sorted_set', 0, -1, withscores=True
                    )[0] == [('key1', 42), ('key2', 49)]

    redis_my.flushall()


def test_redis_get_multiple(redis_my):
    redisclient = RedisClient()

    assert redisclient.set('key1', 'value1') is True
    assert redisclient.set('key2', 'value2') is True
    assert redisclient.set('key3', 'value3') is True
    assert redisclient.set('key4', 'value4') is True

    values = ['value1', 'value2', 'value3', 'value4']

    assert redisclient.get_multiple('key1', 'key2', 'key3', 'key4') == values

    redis_my.flushall()


def test_redis_hm_get(redis_my):
    redisclient = RedisClient()

    assert redisclient.hmset('hash_set', key1='value1', key2='value2') is True
    assert redisclient.hmget('hash_set', 'key1', 'key2')[0] == ['value1', 'value2']
    redis_my.flushall()


def test_redis_zrange(redis_my):
    redisclient = RedisClient()

    assert redisclient.zset('sorted_set', 42, 'key1', 49, 'key2') == 2
    assert redisclient.zrange(
                    'sorted_set', 0, -1
                    ) == [['key1', 'key2']]
    assert redisclient.zrange(
                    'sorted_set', 0, -1, withscores=True
                    )[0] == [('key1', 42), ('key2', 49)]

    redis_my.flushall()


def test_redis_zrem(redis_my):
    redisclient = RedisClient()

    redisclient.zset('sorted_set', 42, 'key1', 49, 'key2', 1, 'key3')

    # values = ['value1', 'value2', 'value4']
    redisclient.zrem('sorted_set', 'key3')

    assert redisclient.zrange(
                    'sorted_set', 0, -1
                    ) == [['key1', 'key2']]
    assert redisclient.zrange(
                    'sorted_set', 0, -1, withscores=True
                    )[0] == [('key1', 42), ('key2', 49)]

    # assert redisclient.get_multiple('key1', 'key2', 'key4') == values

    redis_my.flushall()
