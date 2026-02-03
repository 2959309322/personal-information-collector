from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase

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