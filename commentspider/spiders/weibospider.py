# coding:utf-8
import scrapy
import json
import os

"""爬微博评论可以把延迟选项关闭，不使用cookies
一台机器每小时大概采集9W条评论
"""

try:
    import cPickle
except:
    import pickle as cPickle

from commentspider.items import WeiboItem


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['m.weibo.cn']
    start_urls = ['https://m.weibo.cn/status/4174280579492207']

    def parse(self, response):
        try:
            print os.getcwd()
            with open('cookie.txt', 'rb') as f:
                self.cookies = cPickle.load(f)
                print '成功加载cookie.txt文件'
        except EnvironmentError, why:
            print '没有找到cookie.txt文件%s' % why

        weibo_url = response.url
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Host': 'm.weibo.cn',
            'Referer': weibo_url,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.\
                36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        self.url_id = weibo_url.split('/')[-1]
        url = r'https://m.weibo.cn/api/comments/show?id=%s&page=1' % self.url_id
        request = scrapy.Request(url=url, headers=self.headers,
                                 callback=self.comment_parse)
        yield request

    def comment_parse(self, response):
        """解析json文件，提取评论数据
        """
        comments = json.loads(response.body_as_unicode())

        if comments['ok'] == 1:
            for data in comments['data']:
                comment_id = data['id']
                like_counts = data['like_counts']
                source = data['source']
                text = data['text']
                user = data['user']
                weibo_comment_item = WeiboItem(
                    comment_id=comment_id, like_counts=like_counts,
                    source=source, text=text, user=user,
                )
                yield weibo_comment_item

            # 获取当前页码
            page = response.url.split('=')[-1]
            url = r'https://m.weibo.cn/api/comments/show?id=%s&page=%s' \
                % (self.url_id, int(page) + 1)
            request = scrapy.Request(
                url=url, headers=self.headers, callback=self.comment_parse,
            )
            yield request

        else:
            # 判断是否采集完毕
            page = response.url.split('=')[-1]
            url = r'https://m.weibo.cn/api/comments/show?id=%s&page=%s' \
                % (self.url_id, int(page) + 1)
            request = scrapy.Request(
                url=url, headers=self.headers, callback=self._is_end,
            )
            yield request

    def _is_end(self, response):
        """判断是否采集完毕
        """
        comments = json.loads(response.body_as_unicode())
        if comments['ok'] == 1:
            request = scrapy.Request(
                url=response.url, headers=self.headers,
                callback=self.comment_parse,
            )
            yield request
        else:
            return
