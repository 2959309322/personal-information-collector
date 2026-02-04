from typing import Union
from sqlalchemy import create_engine, text
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
"""
注意，每一个创建出来的数据表对象只能使用一次！！！！！
"""
Engine = create_engine("mysql+pymysql://root:123456@localhost:3306/collector",echo=True)

class Base(DeclarativeBase):
    pass

class Weather(Base):
    __tablename__ = 'weather'

    Id = Column(Integer, primary_key=True)
    Date_time = Column(DateTime)
    City = Column(String(20))
    Temperature = Column(String(20))
    Feel = Column(String(20))
    Desc = Column(String(100))
    WindDir = Column(String(20))
    Visibility = Column(String(20))

    def __repr__(self):
        return (f"实时天气  {self.Date_time}\n城市:{self.City}\n气温:{self.Temperature}\n"
                f"体感:{self.Feel}\n{self.Desc}\n风向:{self.WindDir}\n")

class GithubTrending(Base):
    __tablename__ = 'github_trending'

    Id = Column(Integer, primary_key=True)
    Date_time = Column(DateTime)
    Name = Column(String(20))
    Rank = Column(Integer)
    Url = Column(String(200))
    Description = Column(String(200))
    Language = Column(String(20))
    Stars = Column(String(20))

    def __repr__(self):
        return(f"{self.Date_time}\n"
               f"第{self.Rank}个:{self.Name}\n"
               f"{self.Description}\n"
               f"使用语言{self.Language}    Stars:{self.Stars}\n"
               f"网址{self.Url}\n")

'''
videos.append(base.hotdata(
                    date=date.today(),
                    name=title,
                    rank=rank,
                    url=url,
                    info = {
                        'up_name': up_name,
                        'view_num': view_num,
                        'coin': coin,
                        'share': share,
                        'reply_num': reply_num,

'''
class BiliPop(Base):
    __tablename__ = 'bili_pop'

    Id = Column(Integer, primary_key=True)
    Date_time = Column(DateTime)
    Title = Column(String(20))
    Rank = Column(Integer)
    Url = Column(String(200))
    Up_name = Column(String(20))
    View_num = Column(String(20))
    Coin = Column(String(20))
    Share = Column(String(20))


    def __repr__(self):
        return(f"{self.Date_time}\n"
               f"第{self.Rank}个:{self.Title}\n"
               f"Up:{self.Up_name}\n"
               f"硬币:{self.Coin}  播放量:{self.View_num}  转发量:{self.Share}\n"
               f"网址{self.Url}\n")

Base.metadata.create_all(Engine)
Session = sessionmaker(bind=Engine)

class CRUD:
    """
    这里是一些增删改查的处理
    """
    def __init__(self):
        pass

    def Create(self,data:Union[Weather,GithubTrending,BiliPop]):
        """
        先使用对应表格的类创建好对象，然后传入该函数即可\n
        Create(item)
        """
        try:
            session = Session()
            session.add(data)
            session.commit()
            session.close()
        except Exception as e:
            print(e)
            return None

    def Read_all(self,table:str):
        """
        查询指定数据表所有元素，返回格式为list[dict]\n
        使用方法Read_all(table_name)\n
        Weather,GithubTrending,BiliPop\n
        """
        try:
            session = Session()
            if table == 'Weather':
                data = session.query(Weather).all()
                weather = []
                for item in data:
                    weather.append(item.__dict__)
                return weather
            elif table == 'GithubTrending':
                data = session.query(GithubTrending).all()
                github_trending = []
                for item in data:
                    github_trending.append(item.__dict__)
                return github_trending
            elif table == 'BiliPop':
                data = session.query(BiliPop).all()
                bili_pop = []
                for item in data:
                    bili_pop.append(item.__dict__)
                return bili_pop
            session.close()
        except Exception as e:
            print(e)
            return None

    def Read(self,table:str, idx:int):
        """
        查询指定数据表某一行，返回格式为dict\n
        使用方法Read_all(table_name,idx)\n
        Weather,GithubTrending,BiliPop\n
        """
        try:
            session = Session()
            if table == 'Weather':
                return session.query(Weather).get(idx).__dict__
            elif table == 'GithubTrending':
                return session.query(GithubTrending).get(idx).__dict__
            elif table == 'BiliPop':
                return session.query(BiliPop).get(idx).__dict__
            session.close()
        except Exception as e:
            print(e)
            return None
    def Update(self, table:str, data:Union[Weather,GithubTrending,BiliPop], idx:int):
        """
        对于爬虫，这个函数一般用不到，蓑衣这里只做一个简单实现\n
        用法，创建好一个修改的对象，然后指定对应table中的索引idx\n
        直接覆盖\n
        Weather,GithubTrending,BiliPop
        """
        print("你确定吗(Yes(1)/No(0))\n:")
        value = input()
        if value == 0 : return None
        try:
            session = Session()
            #data.Id = idx
            if table == 'Weather':
                session.query(Weather).filter(Weather.Id==idx).update({
                    Weather.Date_time: data.Date_time,
                    Weather.City: data.City,
                    Weather.Temperature: data.Temperature,
                    Weather.Feel: data.Feel,
                    Weather.Desc: data.Desc,
                    Weather.WindDir: data.WindDir,
                    Weather.Visibility: data.Visibility,
                })
            elif table == 'GithubTrending':
                session.query(GithubTrending).filter(GithubTrending.Id==idx).update({
                    GithubTrending.Date_time: data.Date_time,
                    GithubTrending.Rank: data.Rank,
                    GithubTrending.Url: data.Url,
                    GithubTrending.Description: data.Description,
                    GithubTrending.Language: data.Language,
                    GithubTrending.Stars: data.Stars,
                })
            elif table == 'BiliPop':
                session.query(BiliPop).filter(BiliPop.Id==idx).update({
                    BiliPop.Rank: data.Rank,
                    BiliPop.Url: data.Url,
                    BiliPop.View_num: data.View_num,
                    BiliPop.Coin: data.Coin,
                    BiliPop.Share: data.Share,
                })
            session.commit()
            session.close()
        except Exception as e:
            print(e)
            return None

    def Delete(self, table:str, idx:int):
        """
        删除特定表格中特定idx的数据,谨慎\n
        Delete(table,idx)\n
        Weather,GithubTrending,BiliPop
        """
        print("你确定吗(Yes(1)/No(0))\n:")
        value = input()
        if value == 0: return None
        try:
            session = Session()
            if table == 'Weather':
                data = session.query(Weather).filter(Weather.Id == idx).first()
                if data: session.delete(data)
                session.execute(text("ALTER TABLE weather AUTO_INCREMENT = 1;"))
            elif table == 'GithubTrending':
                data = session.query(GithubTrending).filter(GithubTrending.Id == idx).first()
                if data: session.delete(data)
                session.execute(text("ALTER TABLE github_trending AUTO_INCREMENT = 1;"))
            elif table == 'BiliPop':
                data = session.query(BiliPop).filter(BiliPop.Id == idx).first()
                if data: session.delete(data)
                session.execute(text("ALTER TABLE bili_pop AUTO_INCREMENT = 1;"))
            session.commit()
            session.close()
        except Exception as e:
            print(e)
            return None

    def Delete_all(self, table:str):
        """
        删除特定表格中所有的数据，谨慎\n
        Delete(table)\n
        Weather,GithubTrending,BiliPop
        """
        print("你确定吗(Yes(1)/No(0))\n:")
        value = input()
        if value == 0: return None
        try:
            session = Session()
            if table == 'Weather':
                session.query(Weather).delete()
                session.execute(text("ALTER TABLE weather AUTO_INCREMENT = 1;"))
            elif table == 'GithubTrending':
                session.query(GithubTrending).delete()
                session.execute(text("ALTER TABLE github_trending AUTO_INCREMENT = 1;"))
            elif table == 'BiliPop':
                session.query(BiliPop).delete()
                session.execute(text("ALTER TABLE bili_pop AUTO_INCREMENT = 1;"))
            session.commit()
            session.close()
        except Exception as e:
            print(e)
            return None
