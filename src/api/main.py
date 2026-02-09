from fastapi import FastAPI,Query
from pydantic import BaseModel
from Weather_route import router as weather_router
from Github_route import router as github_router
from Bili_route import router as bili_router
import cache
app = FastAPI(
    title="personal-information-collector",
    description="信息收集",
    version="1.0",
)
app.include_router(weather_router)
app.include_router(github_router)
app.include_router(bili_router)


@app.get("/")
async def root():
    return {"message": "这是一个信息获取助手。可以去 /docs 看看。"}

if __name__ == "__main__":
    import uvicorn
    c = cache.Cache()
    c.fresh()
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,        # 开启热重载
        workers=1           # reload 模式下只能是 1
    )





