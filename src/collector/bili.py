#个人感觉这bili的拉取和weather差不多
#因为get获得的数据都是json
import base
import requests
from datetime import date
class bili(base.collector):
    """
    该类用于获取bilibili热门榜单\n
    使用collect()即可获取热门榜单列表\n
    具体数据类型参考base.py
    """
    def __init__(self):
        super().__init__("bilibili")
        self.headers = {
            'Origin': 'https://www.bilibili.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.bilibili.com/v/popular/all/?spm_id_from=333.1007.0.0',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0',
        }
        self.url = "https://api.bilibili.com/x/web-interface/ranking/v2"

    def collect(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=5)
            cards = response.json()
            response.raise_for_status()

        except Exception as e:
            print(f"get json error:{e}")
            return None
        videos = []
        for idx, card in enumerate(cards['data']['list'], 1):
            try:
                if len(videos) == 10: break
                rank = idx
                title = card.get('title')
                up_name = card.get('owner').get('name')
                view_num = str(card.get('stat').get('view'))
                reply_num = str(card.get('stat').get('reply'))
                coin = str(card.get('stat').get('coin'))
                share = str(card.get('stat').get('share'))
                url = card.get('short_link_v2')
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
                    }
                ))
            except Exception as e:
                print(f"解析第{idx}个热门视频信息错误:{e}")
        return videos
