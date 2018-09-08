from redis import StrictRedis
from redis_lock import Lock, AlreadyAcquired


class RedisClient:
    connection = StrictRedis(host='localhost', port=6379, db=0)

    def set(self, key, value, ex=None, px=None, nx=False, xx=False):
        lock = Lock(self, key, expire=DEFAULT_HERD_LOCK_EXPIRE)

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
