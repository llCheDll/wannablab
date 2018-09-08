from redis import StrictRedis
from config import settings
from redis_lock import Lock, AlreadyAcquired


class RedisClient:
    def __init__(self):
        self.connection = StrictRedis(host=settings.redis.host, port=settings.redis.port, db=0)

    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        lock = Lock(self.connection, key)

        try:
            if lock.acquire():
                result = self.connection.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

                lock.release()
                return result
            return False
        except AlreadyAcquired:
            return False

    def get_multiple(self, keys):
        with self.connection.pipeline(transaction=False) as pipe:
            for key in keys:
                pipe.get(key)
            return pipe.execute()
