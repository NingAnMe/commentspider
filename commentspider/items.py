# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboItem(scrapy.Item):
    """微博评论内容
    """
    # 评论的唯一id
    comment_id = scrapy.Field()
    # 评论被赞次数
    like_counts = scrapy.Field()
    # 评论的来源（设备）
    source = scrapy.Field()
    # 评论的内容
    text = scrapy.Field()
    # 评论的用户
    user = scrapy.Field()


class DoubanItem(scrapy.Item):
    """豆瓣评论内容
    """
    # 评论的唯一id
    comment_id = scrapy.Field()
    # 评论被赞次数
    like_counts = scrapy.Field()
    # 看过or想看
    seen = scrapy.Field()
    # 评分
    rate = scrapy.Field()
    # 评论的内容
    text = scrapy.Field()
    # 评论的用户
    user = scrapy.Field()
    # 评论的时间
    comment_time = scrapy.Field()
