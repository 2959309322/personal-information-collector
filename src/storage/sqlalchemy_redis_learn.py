# from sqlalchemy import create_engine
# from sqlalchemy import text
# engine = create_engine("sqlite+pysqlite:///:memory:", echo=False)
# with engine.connect() as conn:
#     conn.execute(text("CREATE TABLE some_table (x int, y int)"))
#     conn.execute(text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
#         [{"x": 6, "y": 8}, {"x": 9, "y": 10}],)
#     conn.commit()
#     # result = conn.execute(text("SELECT x FROM some_table"))
#     # result = conn.execute(text("SELECT y FROM some_table"))
#     result = conn.execute(text("SELECT * FROM some_table"))#或者x,y也可以
#     # for row in result:
#     #     print(row[0])
#     #     print(row.x)
#     # for x,y in result:
#     #     ...
#     # for dict_row in result.mappings():
#     #     print(dict_row['x'])
#     # 因为这个result是个游标，只能遍历一次，
#     # 所以可以先把他遍历一次存储来，方便后续多次操作
#     print(result.all())
"""
以上都是用sql原生语言去操作的
下面使用ORM操作，把sql的示例对应到py的class上
"""
import time

# from sqlalchemy import MetaData, Table, Column, Integer, String
# from sqlalchemy.orm import declarative_base, sessionmaker


#redis
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True, encoding='utf-8')
r.set('foo','bar')#redis内部存储的所有值都是字节序列，所以会打出b开头
print(r.get('foo'))#两种取出键对应值方法等价#可以访问服务器的时候使用decode_response
print(r['foo'])
print(type(r.get('foo')))#不设置decode_response时class bytes
r.set('test','test',ex = 5)
time.sleep(4)
print(r.get('test'))
#####对于string#####无序
"""
ex->过期时间(s)
px->过期时间(ms)
nx->(bool) 若设置为True时只有当name不存在，当前set操作才会执行
xx->(bool) 若设置为True时只有当name存在时，当前set操作才会执行
"""
#setnx()->nx=true
#setex()->ex=...
#psetex()->px=...
#mset({*:*,*:*,...})批量设置
#mget({*,*,...})批量查询
# r.mset({'A':'A','B':'B'})
# ls = r.mget(['A','B'])->list
# print(ls)
#设置新值并获取原来的值getset(name,value)

#getrange(key,start,end)-----start和end都是按字节算的
#setrange同理
#getbit(key,offset)
#setbit(key,offset,value)----value = 0/1

#incr(self,name,amount=(int))
#自增 name 对应的值，当 name 不存在时，则创建 name＝amount
#incrbyfloat()
#decr()只有int版的
#append(key,value)在key的value后追加

#########对于hash##########
#和set命令相似，在最前面加个h即可
#且hmget(name, keys, *args)，hmset(name, mapping)
#差异
#hgetall(name)    name是hash表的名
#hlen(name),hkeys,hvals,hexists(name,key)
#hincrby,hincrbyfloat


########对于list##########
#lpush(name,...,...,...)从左边加，没有就新建
#lrange(name,start,end)#切片取值
#lpushx()从左边加，没有也无法创建
#linsert(name, where, refvalue, value) where="before"/"after"
#lset(name,idx,value)
#lrem(name,value,num)num是删除个数，正->从左到右,负->从右到左
#lpop从左删除并返回
#ltrim(name,start,end)删除不在区间的值
#lindex(name,idx)取值
#blpop(names,timeout)移除多个列表

#zset有序set。。。。。自己看看把

#一些操作
#delete(*name)删除
#exists(name)看是否存在

