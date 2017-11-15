# coding:utf-8
import scrapy
import json
import os

"""爬取豆瓣电影的评论，必须使用cookies,
最好设置延迟1秒
"""

try:
    import cPickle
except:
    import pickle as cPickle

from commentspider.items import DoubanItem



class WeiboSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/25821634/']

    def parse(self, response):
        try:
            print os.getcwd()
            with open('cookie.txt', 'rb') as f:
                self.cookies = cPickle.load(f)
                print '成功加载cookie.txt文件'
        except EnvironmentError, why:
            print '没有找到cookie.txt文件%s' % why

        s = '%s' % response.url
        self.movie_id = s.split('/')[-2]

        comment_url = '%scomments?sort=new_score&status=P' % response.url
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Referer': response.url,
            'Host': 'movie.douban.com',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        }
        request = scrapy.Request(
            url=comment_url, headers=self.headers, cookies=self.cookies,
            callback=self.comment_parse,
        )
        yield request

    def comment_parse(self, response):
        comments = response.xpath('//div[@class="comment-item"]')
        if comments is not None:
            for comment in comments:
                comment_id = comment.xpath('@data-cid').extract_first()

                like_counts = comment.xpath(
                    '//span[@class="votes"]').extract_first()

                seen = comment.xpath(
                    '//span[@class="comment-info"]/span[1]/text()'
                ).extract_first()

                rate = comment.xpath(
                    '//span[@class="comment-info"]/span[2]/@title'
                ).extract_first()

                text = comment.xpath(
                    '//div[@class="comment"]/p/text()'
                ).extract_first()

                user = comment.xpath(
                    '//span[@class="comment-info"]/a/text()'
                ).extract_first()

                comment_time = comment.xpath(
                    '//span[@class="comment-info"]/span[3]/text()'
                ).extract_first()

                douban_comment_item = DoubanItem(
                    comment_id=comment_id, like_counts=like_counts,
                    seen=seen, rate=rate, text=text, user=user,
                    comment_time=comment_time,
                )
                if comment_id is not None:
                    yield douban_comment_item

        url = response.xpath(
            '//div[@id="paginator"]/a[@class="next"]/@href').extract_first()
        if url is not None:
            next_url = r'https://movie.douban.com/subject/%s/comments%s' \
                % (self.movie_id, url)
            self.headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
                'Connection': 'keep-alive',
                'Referer': response.url,
                'Host': 'movie.douban.com',
                'Upgrade-Insecure-Requests': 1,
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            }
            request = scrapy.Request(
                url=next_url, headers=self.headers, cookies=self.cookies,
                callback=self.comment_parse,
            )
            yield request
