# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings

class OldsPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if item.get("olds_thread", None) is None:
            return item

        #To avoid incomplete / unecessary items
        #todo
        #    do this job in spider
        if item.get("oriSource", None) is None:
            return item

        spec = {"olds_thread":item["olds_thread"]}
        self.collection.new.update(spec, {"$set":dict(item)},upsert = True)
        return None
