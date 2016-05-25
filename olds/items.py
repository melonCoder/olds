# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class OldsItem(Item):
    olds_thread = Field()
    title = Field()
    editor = Field()
    source = Field()
    #time
    year = Field()
    month = Field()
    day = Field()
    passage = Field()
    pass
