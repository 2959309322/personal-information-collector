from datetime import date
from fastapi import Query, APIRouter
from pydantic import BaseModel
import cache
import database as db
import bili

today = date.today()


class BiliResponse(BaseModel):
    Date_time: date
    Rank: int
    Title: str
    Up_name: str
    Coin: str
    Share: str
    Url: str
    View_num:str

#一些初始化
crud = db.CRUD()
bili = bili.bili()
router = APIRouter(prefix="/bili", tags=["Bili"])
c = cache.Cache()

@router.get("/bili", response_model=list[BiliResponse])
async def get_bili():#单个城市天气获取
    bili_data = c.Bili_get_all()
    bili_list = []
    print(bili_data)
    if bili_data is None:
        bili_data = bili.collect()
        for item in bili_data:
            data = BiliResponse(Date_time=item.date, Rank=item.rank, Title=item.name,
                                Up_name=item.info["up_name"],Coin=item.info['coin'],
                                Share=item.info["share"],Url=item.url,View_num=item.info['view_num'])
            data_crud = db.BiliPop(Date_time=item.date, Rank=item.rank, Title=item.name,Url=item.url,
                                   Up_name=item.info["up_name"], Coin=item.info['coin'],
                                   Share=item.info["share"],View_num=item.info['view_num'])
            crud.Create(data_crud)
            bili_list.append(data)
        return bili_list
    elif bili_data[-1]['Date_time'].date() != today:
        print(bili_data[-1]['Date_time'])
        print(today)
        bili_data = bili.collect()
        for item in bili_data:
            data = BiliResponse(Date_time=item.date, Rank=item.rank, Title=item.name,
                                Up_name=item.info["up_name"], Coin=item.info['coin'],
                                Share=item.info["share"], Url=item.url, View_num=item.info['view_num'])
            data_crud = db.BiliPop(Date_time=item.date, Rank=item.rank, Title=item.name, Url=item.url,
                                   Up_name=item.info["up_name"], Coin=item.info['coin'],
                                   Share=item.info["share"], View_num=item.info['view_num'])
            crud.Create(data_crud)
            bili_list.append(data)
        return bili_list
    for item in bili_data:
        data = BiliResponse(Date_time=item["Date_time"], Rank=item["Rank"], Title=item["Title"],
                                Up_name=item["Up_name"], Coin=item["Coin"],
                                Share=item["Share"], Url=item["Url"], View_num=item["View_num"])
        bili_list.append(data)
    return bili_list
