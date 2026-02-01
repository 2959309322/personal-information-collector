import requests
from bs4 import BeautifulSoup
import base

class github(base.collector):
    """
    该类用于获取github项目热门榜单\n
    使用collect()即可获得数据列表，数据类型参考base.py\n
    如出现网络错误，注意优先检查网络环境\n
    """

    def __init__(self):
        super().__init__("github")
        self.url = "https://github.com/trending?since=daily"
        # 设置请求头，模拟正常浏览器访问，避免被识别成爬虫程序
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def collect(self) -> list[base.hotdata]:
        html = self.get_html(self.url)
        data_list = self.unpack_html(html)
        return data_list

    # 获取页面数据
    def get_html(self,url):
        try:
            responese = requests.get(url, headers=self.headers, timeout=5)
            # 为了反爬，在多次请求间，一般会加上几秒的延迟
            responese.raise_for_status()
            responese.encoding = 'utf-8'
            return responese.text
        except requests.exceptions.Timeout:
            print(f"请求超时(5)秒，检查网络")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP错误({e.response.status_code})")
        except Exception as e:
            print(f"请求失败:{e}")

    def unpack_html(self,html):
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all('article', class_="Box-row")
        print(len(articles))
        projects = []
        for idx, article in enumerate(articles, 1):
            try:
                # 可以找到<h3><a>内容</a></h3>
                # 也可以换成.find('h2).find('a')
                project_tag = article.select_one('h2 a')
                # 此时这个project_tag也是<><>...<><>的格式
                if not project_tag:
                    continue

                # 提取 作者/仓库(author/repo)
                text = project_tag.get_text(strip=True)  # 获取tag里所有文本
                # strip去掉文本前后的空格，这时返回的是一个字符串，但是可能串内存在连续空格
                project_name = ' '.join(text.split())
                """
                首先内部split默认按空格/换行符分割
                分割后再统一用' '分割拼接在一起
                """
                # 对于p，因为他有很多个class，所以要加.来明确类
                # 当然也可以用特殊标识的方式，
                # 但是！！！特殊标识要求一摸一样，而类可以只包含特殊标识中的一个
                # "col-9 color-fg-muted my-1 pr-4"
                # 用特殊标识的话可能因为这几个元素前后顺序错误导致读不到
                desc_tag = article.select_one('p.col-9.color-fg-muted')
                if desc_tag:
                    desc = desc_tag.get_text(strip=True)
                else:
                    desc = ""

                # 而对于span，他有很多个span，所以需要span[特殊标识]
                lang_tag = article.select_one('span[itemprop="programmingLanguage"]')
                if lang_tag:
                    lang = lang_tag.get_text(strip=True)
                else:
                    lang = 'unknown'
                """
                [href $="/stargazers"]	href以"/stargazers"结尾
                [href ^="/"]	href以"/"开头
                [href *="github"]	href包含"github"	
                [href ~="button"]	href包含单词"button"
                [href |="en"]	href以"en"或"en-"开头
                """
                star_tag = article.select_one('a[href $="/stargazers"]')
                if star_tag:
                    text = star_tag.get_text(strip=True)
                    star = "".join(text.split(','))
                else:
                    star = None
                # 这种后缀表达式还挺新奇的
                repo_url = "https://github.com" + project_tag['href'] if project_tag.get('href') else ""

                projects.append(base.hotdata(
                    name = project_name,
                    rank = idx,
                    url = repo_url,
                    info = {
                        'description': desc,
                        'language': lang,
                        'stars': star,
                    }
                ))
            except Exception as e:
                print(f"跳过第{idx}个项目(解析错误) : {str(e)[:50]}")
                continue
        return projects
