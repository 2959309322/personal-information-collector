import bili, github, weather, database
from datetime import date

crud_instance = database.CRUD()
bili_instance = bili.bili()
github_instance = github.github()
weather_instance = weather.hfweather()
today = date.today()


if crud_instance.Read("BiliPop",1) is None:
    bili_ls = bili_instance.collect()
    for item in bili_ls:
        bili_data = database.BiliPop(Date_time=item.date, Title=item.name,
                                     Rank=item.rank, Url=item.url, Up_name=item.info['up_name'],
                                     View_num=item.info['view_num'],
                                     Coin=item.info['coin'], Share=item.info['share'])
        crud_instance.Create(bili_data)
elif crud_instance.Read("BiliPop", 1)['Date_time'].date() != today:
    bili_ls = bili_instance.collect()
    for item in bili_ls:
        bili_data = database.BiliPop(Date_time=item.date, Title=item.name,
                                     Rank=item.rank, Url=item.url, Up_name=item.info['up_name'],
                                     View_num=item.info['view_num'],
                                     Coin=item.info['coin'], Share=item.info['share'])
        crud_instance.Create(bili_data)

if crud_instance.Read("GithubTrending",1) is None:
    github_ls = github_instance.collect()
    for item in github_ls:
        github_data = database.GithubTrending(Date_time=item.date, Name=item.name, Rank=item.rank, Url=item.url,
                                              Description=item.info['description'], Language=item.info['language'],
                                              Stars=item.info['stars'])
        crud_instance.Create(github_data)
elif crud_instance.Read("GithubTrending", 1)["Date_time"].date() != today:
    github_ls = github_instance.collect()
    for item in github_ls:
        github_data = database.GithubTrending(Date_time=item.date, Name=item.name, Rank=item.rank, Url=item.url,
                                              Description=item.info['description'], Language=item.info['language'],
                                              Stars=item.info['stars'])
        crud_instance.Create(github_data)

if crud_instance.Read("Weather",1) is None:
    weather_ls = weather_instance.collect(batch=True, target=["北京", "上海", "广州", "深圳"])
    for item in weather_ls:
        weather_data = database.Weather(Date_time=item["date"], City=item["city"],
                                        Temperature=item["temp"], Feel=item["feelsLike"],
                                        Desc=item["text"], WindDir=item["windDir"], Visibility=item["vis"])
        crud_instance.Create(weather_data)
elif crud_instance.Read("Weather", 1)["Date_time"].date() != today:
    weather_ls = weather_instance.collect(batch=True, target=["北京", "上海", "广州", "深圳"])
    for item in weather_ls:
        weather_data = database.Weather(Date_time=item["date"], City=item["city"],
                                        Temperature=item["temp"], Feel=item["feelsLike"],
                                        Desc=item["text"], WindDir=item["windDir"], Visibility=item["vis"])
        crud_instance.Create(weather_data)

database.shutdown_server()
# crud_instance.Delete_all("BiliPop")
# crud_instance.Delete_all("GithubTrending")
# crud_instance.Delete_all("Weather")
