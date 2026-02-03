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
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker



