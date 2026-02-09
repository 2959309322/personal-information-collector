from datetime import date
from fastapi import Query, APIRouter
from pydantic import BaseModel
import cache
import database as db
import github

today = date.today()


class GithubResponse(BaseModel):
    Date_time:date
    Rank: int
    Name: str
    Description: str
    Language: str
    Stars: str
    Url: str

#一些初始化
crud = db.CRUD()
git = github.github()
router = APIRouter(prefix="/github", tags=["Github"])
c = cache.Cache()

@router.get("/github", response_model=list[GithubResponse])
async def get_github():#单个城市天气获取
    git_data = c.Github_get_all()
    github_list = []
    print(git_data)
    if git_data is None:
        git_data = git.collect()
        for item in git_data:
            data = GithubResponse(Date_time=item.date, Rank=item.rank, Name=item.name,
                                  Description=item.info['description'], Language=item.info['language'], Stars=item.info['stars'],
                                  Url=item.url)
            data_crud = db.GithubTrending(Date_time=item.date, Rank=item.rank, Name=item.name,Url=item.url,
                                          Description=item.info['description'], Language=item.info['language'], Stars=item.info['stars'])
            crud.Create(data_crud)
            github_list.append(data)
        return github_list
    elif git_data[-1]['Date_time'].date() != today:
        print(git_data[-1]['Date_time'])
        print(today)
        git_data = git.collect()
        for item in git_data:
            data = GithubResponse(Date_time=item.date, Rank=item.rank, Name=item.name,
                                  Description=item.info['description'], Language=item.info['language'],
                                  Stars=item.info['stars'],
                                  Url=item.url)
            data_crud = db.GithubTrending(Date_time=item.date, Rank=item.rank, Name=item.name, Url=item.url,
                                          Description=item.info['description'], Language=item.info['language'],
                                          Stars=item.info['stars'])
            crud.Create(data_crud)
            github_list.append(data)
        return github_list
    for item in git_data:
        data = GithubResponse(Date_time=item['Date_time'],Rank=item['Rank'],Name=item['Name'],Description=item['Description'],Language=item['Language'],Stars=item['Stars'],Url=item['Url'])
        github_list.append(data)
    return github_list
