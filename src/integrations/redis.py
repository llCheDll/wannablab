from redis import StrictRedis
from config import settings
from redis_lock import Lock, AlreadyAcquired


class RedisClient:
    def __init__(self):
        self._connection = StrictRedis(host=settings.redis.host,
                                       port=settings.redis.port,
                                       db=0,
                                       decode_responses=True
                                       )

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        """
        Set the value at key ``name`` to ``value``

        :param name: key
        :param value: value
        :param ex: sets an expire flag on key
                   ``name`` for ``ex`` seconds.
        :param px:       --//--        milliseconds.
        :param nx: if set to True, set the value at key
                   ``name`` to ``value`` only if it does not exist.
        :param xx: if set to True, set the value at key
                    ``name`` to ``value`` only if it already exists.
        :return: True if it set`s.
        """
        lock = Lock(self._connection, name)

        try:
            if lock.acquire():
                result = self._connection.set(name, value, ex=ex, px=px, nx=nx, xx=xx)

                lock.release()
                return result
            return False
        except AlreadyAcquired:
            return False

    def getset(self, name, value):
        """
        Sets the value at key ``name`` to ``value``.

        :param name: key
        :param value: value
        :return: The old value at key ``name``.
        """
        lock = Lock(self._connection, name)

        try:
            if lock.acquire():
                result = self._connection.getset(name, value)
                lock.release()

                return result
            return False
        except AlreadyAcquired:
            return False

    def hmset(self, name, **kwargs):
        """
        Set key to value within hash ``name`` for each corresponding
        key and value from the ``**kwargs`` dict.

        :param name: hash(name)
        :param kwargs: key=value
        :return: True if it set`s
        """
        lock = Lock(self._connection, name)

        try:
            if lock.acquire():
                result = self._connection.hmset(name, kwargs)

                lock.release()
                return result
            return False
        except AlreadyAcquired:
            return False

    def zset(self, name, *args):
        """
        Zset method of the RedisClient class.
        **************************************
        :param name: It`s name of sorted set.
        :param args: This method accepts arguments
                     in the form of score1, name1 ... score(n), name(n).
        :return: Counter of added pairs.
        Usage:
            >>redis_client.zset('sorted_set', 42, 'arg1', 42.0, 'arg2')
            >>2
        """
        lock = Lock(self._connection, name)

        try:
            if lock.acquire():
                result = self._connection.execute_command('ZADD', name, *args)

                lock.release()
                return result
            return False
        except AlreadyAcquired:
            return False

    def get_multiple(self, *keys):
        """
        Get`s the list of values from list of keys.
        :param keys: List of keys
        :return: List of values
        """
        with self._connection.pipeline(transaction=False) as pipe:
            for key in keys:
                pipe.get(key)
            return pipe.execute()

    def hmget(self, name, *args):
        """
        Get`s the list of
        :param name: Hash of hash set
        :param args: List of keys
        :return: List of values
        """
        with self._connection.pipeline(transaction=False) as pipe:
            pipe.hmget(name, args)
            return pipe.execute()

    def zrange(self, name, start=0, end=-1, desc=False, withscores=False, score_cast_func=float):
        """
        Return a range of values from sorted set ``name`` between
        ``start`` and ``end`` sorted in ascending order.

        :param name:    Name of sorted set.
        :param start:   Start of member`s list.
                    By default 0 (the first element)
        :param end:     End of member`s list.
                    By default -1 (the last element)
        :param desc:    A boolean indicating whether to
                    sort the results descendingly
        :param withscores: Indicates to return the scores along with the member.
                        The return type is a list of (member, score) pairs
        :param score_cast_func: A callable used to cast the score return value
        :return: List of members or list of pairs (member, score)
        """
        with self._connection.pipeline(transaction=False) as pipe:
            pipe.zrange(
                name=name, start=start,
                end=end, desc=desc,
                withscores=withscores, score_cast_func=score_cast_func
            )
            return pipe.execute()
