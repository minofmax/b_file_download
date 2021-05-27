import json
import random
import re
import traceback
from typing import List

import requests
from pyquery import PyQuery as pq
from requests import RequestException

USER_AGENT = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]
BILIBILI_BASE_URL = 'https://www.bilibili.com/'
VIDEO_SUFFIX = '.flv'
AUDIO_SUFFIX = '.flac'
VIDEO_QUERY_URL = 'https://api.bilibili.com/x/space/arc/search?mid=229733301&ps=100&tid=0&pn=1&keyword={keyword}&' \
                  'order=pubdate&jsonp=jsonp'
# 自定义下载地址，支持自定义
DOWNLOAD_FILE_SAVING_PATH = 'E:\\Users\\nical\\'


class Bilibili(object):
    """
    最可能需要定制化修改的，应该是@get_video_list方法，因为这个方法是获取视频列表和每个视频对应bvid信息的接口
    目前是定制化的获取某位up主的视频列表，后续按自己的需求修改
    """

    def __init__(self, cookie):
        """
        在初始化方法里定义了一些headers，在后续实例方法里调用
        :param cookie: 自定义cookie
        """
        self.user_agent = random.choice(USER_AGENT)
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q = 0.9',
            'Cookie': cookie
        }
        self.get_html_headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q = 0.9'
        }
        self.download_headers = {
            'origin': 'https://www.bilibili.com',
            'User-Agent': self.user_agent
        }

    def get_video_list(self, keyword: str) -> List[dict]:
        """
        因为脚本的需求是爬取某位up主上传的一些视频和音频，所以查询接口会携带该up主信息，如果需要爬别的，可以先调研接口再修改
        主要功能是获取bvid信息
        :param keyword: 接口传入的查询关键字
        :return: 一个bvid字典集合
        """
        video_list_query_url = VIDEO_QUERY_URL.format(keyword=keyword)
        print(video_list_query_url)
        resp = requests.get(video_list_query_url, headers=self.headers)
        if resp.status_code != 200:
            raise Exception('接口返回异常')
        data = json.loads(resp.text)
        video_list = data.get('data').get('list').get('vlist')
        results = []
        for video_info in video_list:
            bvid = video_info.get('bvid')
            results.append({
                'bvid': bvid
            })
        return results

    def get_html(self, url: str) -> str:
        """
        因为需要获取视频和音频文件的下载接口，而下载接口又都在视频访问页当中，访问页的url是baseurl和bvid的拼接
        所以可以根据上面获取的bvid来访问所有的视频页面，然后获取视频的流接口
        :param url: 拼接好的url
        :return: 返回当前视频页的静态html代码
        """
        try:
            response = requests.get(url=url, headers=self.get_html_headers)
            if response.status_code == 200:
                return response.text
        except RequestException:
            msg = traceback.format_exc()
            print('请求Html错误:{}'.format(msg))
            return ''

    def parse_html(self, html: str, bvid: str) -> dict:
        """
        解析当前get_html获得的视频的html代码
        :param html: html代码
        :param bvid: bvid，比较冗余，是因为后面下载可能需要用到
        :return: 返回一由title、视频下载url、音频下载url、bvid的字典
        """
        doc = pq(html)
        video_title = doc('#viewbox_report > h1 > span').text()

        # 用正则匹配来获取play_info集合
        pattern = r'\<script\>window\.__playinfo__=(.*?)\</script\>'
        stream_urls_text = re.findall(pattern, html)[0]
        temp = json.loads(stream_urls_text)
        # 默认很七个url,分别对应七中不同的清晰度（如果有七个的话，视频有几种清晰度应该就有几个url，默认选择最高清）
        video_url = temp.get('data').get('dash').get('video')[0].get('baseUrl')
        audio_url = temp.get('data').get('dash').get('audio')[0].get('baseUrl')
        return {
            'title': video_title,
            'video_url': video_url,
            'audio_url': audio_url,
            'bvid': bvid
        }

    def download(self, bvid: str, download_url: str, file_name: str):
        """
        下载文件的方法
        :param bvid: 这个需要构造referer，b站后台是有openresty做反代或者waf，会根据referer来检验请求合法性
        :param download_url: 下载的url
        :param file_name: 文件名，只需要传入文件名即可，方法内部会根据成员变量BILIBILI_BASE_URL来拼接
        :return: 无返回，会将文件下载到对应的地址
        """
        self.download_headers['Referer'] = BILIBILI_BASE_URL + bvid
        file_path = DOWNLOAD_FILE_SAVING_PATH + file_name
        with open(file_path, 'wb') as f:
            f.write(requests.get(url=download_url, headers=self.download_headers, stream=True, verify=False).content)
        print('{}下载完毕'.format(file_name))


if __name__ == '__main__':
    # 自己登陆后获取cookie，可以在浏览器里用f12查看
    cookie = ""
    b = Bilibili(cookie=cookie)
    # 传入‘4K60FPS’作为查询条件
    results = b.get_video_list('4K120FPS')
    downloads_info = []
    # 获取所有的下载信息
    for result in results:
        bvid = result.get('bvid')
        url = BILIBILI_BASE_URL + bvid
        html = b.get_html(url)
        downloads_info.append(b.parse_html(html, bvid=bvid))
    print(downloads_info)
    # 下载文件，目前只下载了音频，如果需要视频，可以把video_download_url传入调用即可
    for info in downloads_info:
        video_file_name = info.get('title', 'test') + VIDEO_SUFFIX
        audio_file_name = info.get('title', 'test') + AUDIO_SUFFIX
        video_download_url = info.get('video_url')
        audio_download_url = info.get('audio_url')
        bvid = info.get('bvid')
        b.download(bvid, audio_download_url, audio_file_name)
    print('所有文件下载完毕！！！')
