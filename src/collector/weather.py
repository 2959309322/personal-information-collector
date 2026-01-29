import requests

API_KEY = "119bc292b548443e9431f7dbad84cd8a"
API_HOST = "mb564v2nnp.re.qweatherapi.com"
def get_city_id(city_name):
    url = f"https://{API_HOST}/geo/v2/city/lookup"
    params = {"location": city_name, "key":API_KEY, "range":"cn"}
    try:
        #会使网页变成http...?location=...&key=...
        response = requests.get(url, params=params, timeout=5)
        #如果响应的状态码表示请求失败
        # 则该方法会引发一个异常
        response.raise_for_status()
        data = response.json()
        '''
        # 常见的 HTTP 状态码
        200: OK                   # 请求成功
        201: Created             # 创建成功
        400: Bad Request         # 客户端错误
        401: Unauthorized        # 未授权
        404: Not Found           # 未找到
        500: Internal Server Error  # 服务器错误
        '''
        if data.get("code") == "200":#666他的这玩意是字符串不能用数字来对比
            return data["location"][0]["id"]
        else:
            print(f"城市 '{city_name}' 未找到")
            return None
    except Exception as e:
        print(f"获取城市ID失败:{e}")
        return None

def get_rt_weather_single(city_name):
    city_id = get_city_id(city_name)
    url = f"https://{API_HOST}/v7/weather/now/"
    params = {"location": city_id, "key":API_KEY, "range":"cn"}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("code") == "200":#用get如果不存在会返回None，不会崩溃更安全
            keys = ["temp", "feelsLike", "text", "windDir", "vis"]
            info = [{}]
            info[0]["city"] = city_name
            if(data.get("updateTime")):
                temp = data["updateTime"]
                t1 = (temp.split("T"))
                info[0]["date"] = t1[0]
                info[0]["update_time"] = t1[1]
            else: print("no UpdateTime")
            info[0].update({key: data["now"][key] for key in keys if key in data["now"]})
            return info
        else:
            print(f"requests_error_code: {data.get('code')}")
            print("failed to get weather info")
            return None
    except Exception as e:
        print(f"error: {e}")
        return None

def get_rt_weather_batch(city_name):
    city_id = [get_city_id(name) for name in city_name]
    url = f"https://{API_HOST}/v7/weather/now/"
    params = {id:{"location": id, "key":API_KEY, "range":"cn"} for id in city_id}
    index = 0
    tot_info = []
    for param in params:
        info = {}
        try:
            response = requests.get(url, params=params[param], timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("code") == "200":  # 用get如果不存在会返回None，不会崩溃更安全
                keys = ["temp", "feelsLike", "text", "windDir", "vis"]
                info['city'] = city_name[index]
                if (data.get("updateTime")):
                    temp = data["updateTime"]
                    t1 = (temp.split("T"))
                    info["date"] = t1[0]
                    info["update_time"] = t1[1]
                else:
                    print("no UpdateTime")
                info.update({key: data["now"][key] for key in keys if key in data["now"]})
            else:
                print(f"requests_error_code: {data.get('code')}")
                print(f"failed to get {city_name[index]}'s weather info")
        except Exception as e:
            print(f"error: {e}")
        index += 1
        tot_info.append(info)
    return tot_info