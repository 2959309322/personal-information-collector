from datetime import date

from fastapi import Query, APIRouter
from pydantic import BaseModel
import cache
import database as db
import weather
today = date.today()

class WeatherResponse(BaseModel):
    Date_time:date
    City: str
    Temperature: str
    Feel: str
    Desc: str
    WindDir: str
    Visibility: str
#一些初始化
crud = db.CRUD()
wth = weather.hfweather()
router = APIRouter(prefix="/weather", tags=["Weather"])
c = cache.Cache()

@router.get("/weather/{city}")
async def get_weather(city: str):#单个城市天气获取
    info = c.Weather_get_all()
    if info is None:
        city_data = wth.collect(batch=False, target=city)
        city_crud = db.Weather(Date_time=city_data[0]["date"], City=city_data[0]["city"],
                               Temperature=city_data[0]["temp"], Feel=city_data[0]["feelsLike"],
                               Desc=city_data[0]["text"], WindDir=city_data[0]["windDir"],
                               Visibility=city_data[0]["vis"])
        crud.Create(city_crud)
        return WeatherResponse(Date_time=city_data[0]["date"], City=city_data[0]["city"],
                               Temperature=city_data[0]["temp"], Feel=city_data[0]["feelsLike"],
                               Desc=city_data[0]["text"], WindDir=city_data[0]["windDir"],
                               Visibility=city_data[0]["vis"])

    city_info = next((d for d in info if d.get("City") == city), None)
    if city_info is None:#这里是判断是否有这个城市的天气信息
        city_data = wth.collect(batch=False,target=city)
        city_crud = db.Weather(Date_time=city_data[0]["date"], City=city_data[0]["city"],
                                        Temperature=city_data[0]["temp"], Feel=city_data[0]["feelsLike"],
                                        Desc=city_data[0]["text"], WindDir=city_data[0]["windDir"], Visibility=city_data[0]["vis"])
        crud.Create(city_crud)
    elif city_info["Date_time"].date() != today:
        city_data = wth.collect(batch=False, target=city)
        city_crud = db.Weather(Date_time=city_data[0]["date"], City=city_data[0]["city"],
                               Temperature=city_data[0]["temp"], Feel=city_data[0]["feelsLike"],
                               Desc=city_data[0]["text"], WindDir=city_data[0]["windDir"],
                               Visibility=city_data[0]["vis"])
        crud.Create(city_crud)
    return WeatherResponse(Date_time=city_info["Date_time"],City=city_info["City"],Temperature=city_info["Temperature"], Feel=city_info["Feel"],
                                        Desc=city_info["Desc"], WindDir=city_info["WindDir"], Visibility=city_info["Visibility"])

@router.get("/weather", response_model=list[WeatherResponse])
async def get_weather_batch(cities: str = Query(..., description="用逗号分隔的城市列表，例如：北京,上海")):
    city_list = cities.split(",")
    weather_list = []
    for city in city_list:#循环调用上面的单个城市获取
        weather_info = await get_weather(city.strip())
        weather_list.append(weather_info)
    return weather_list