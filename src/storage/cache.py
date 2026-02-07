import json

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

    def Weather_get_all(self):
        key = "Weather"
        if self.Weather.exists(key):
            data = self.Weather.get(key)
            return json.loads(data)

        result = self.db_crud.Read_all("Weather")
        if result is None: return None
        rows = [dict(row) for row in result]

        self.Weather.setex(key, 300, json.dumps(rows, ensure_ascii=False, default=str))
        return rows

    def Github_get_all(self):
        key = "Github"
        if self.Github.exists(key):
            data = self.Github.get(key)
            return json.loads(data)

        result = self.db_crud.Read_all("GithubTrending")
        if result is None: return None
        rows = [dict(row) for row in result]

        self.Github.setex(key, 300, json.dumps(rows, ensure_ascii=False, default=str))
        return rows

    def Bili_get_all(self):
        key = "Bili"
        if self.Bili.exists(key):
            data = self.Bili.get(key)
            return json.loads(data)

        result = self.db_crud.Read_all("BiliPop")
        if result is None: return None
        rows = [dict(row) for row in result]

        self.Bili.setex(key, 300, json.dumps(rows, ensure_ascii=False, default=str))
        return rows