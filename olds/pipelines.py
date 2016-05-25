# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from store import OldsDB

class OldsPipeline(object):
    def process_item(self, item, spider):
        if spider.name != "olds":
            return item
        if item.get("olds_thread", None) is None:
            return item
        spec = {"olds_thread":item["olds_thread"]}
        OldsDB.new.update(spec, {"$set":dict(item)},upsert = True)
        return None
