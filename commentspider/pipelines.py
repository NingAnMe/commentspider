# -*- coding: utf-8 -*-
import pymongo
from commentspider.items import WeiboItem, DoubanItem


class CommentPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'comment')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):

        if isinstance(item, WeiboItem):
            self._process_weibo_item(item)
            return item

        elif isinstance(item, DoubanItem):
            self._process_douban_item(item)
            return item

    def _process_weibo_item(self, item):
        self.db.weibo.insert(dict(item))

    def _process_douban_item(self, item):
        self.db.douban.insert(dict(item))
