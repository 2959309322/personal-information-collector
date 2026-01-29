import pandas as pd
import requests

headers = {
    'Origin': 'https://www.bilibili.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.bilibili.com/v/popular/all/?spm_id_from=333.1007.0.0',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0',

}
def get_bili_hot_info():
    url = "https://api.bilibili.com/x/web-interface/ranking/v2"
    params = {'rid':0,'type':'all'}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        cards = response.json()
        response.raise_for_status()

    except Exception as e:
        print(f"get json error:{e}")
    videos = []
    for idx,card in enumerate(cards['data']['list'],1):
        try:
            rank = view_num = card.get('stat').get('his_rank')
            title = card.get('title')
            up_name = card.get('owner').get('name')
            view_num = card.get('stat').get('view')
            reply_num = card.get('stat').get('reply')
            coin = card.get('stat').get('coin')
            share = card.get('stat').get('share')
            url = card.get('short_link_v2')
            videos.append({
                "rank": rank,
                'title': title,
                'up_name': up_name,
                'view_num': view_num,
                'coin': coin,
                'share': share,
                'reply_num': reply_num,
                'url': url,
            })
        except Exception as e:
            print(f"解析第{idx}个热门视频信息错误:{e}")
    return videos