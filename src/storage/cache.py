import database
import redis

class Cache:
    def __init__(self):
        #定义redispool、每一个采集器的缓冲区
        self.pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True, encoding = 'utf-8')
        self.Weather = redis.Redis(connection_pool=self.pool)
        self.Github = redis.Redis(connection_pool=self.pool)
        self.Bili = redis.Redis(connection_pool=self.pool)
        self.db_crud = database.CRUD()
