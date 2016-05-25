 # -*- coding: utf-8 -*-
import re
from scrapy.selector import Selector
from olds.items import OldsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class OldsSpider(CrawlSpider):
    name = "olds"
    allowed_domains = ["tech.163.com"]
    start_urls = ['http://tech.163.com']
    rules = (
        Rule(
            LinkExtractor(allow=r"/16/05\d+/\d+/*"),
            callback = "parse_item",
            follow = False ##whether to continue recursively
            ),
    )

    def parse_item(self, response):
        item = OldsItem()
        item['olds_thread'] = response.url.strip().split('/')[-1][:-5]
        self.get_title(response, item)
        self.get_editor(response, item)
        self.get_source(response, item)
        self.get_date(response, item)
        self.get_passage(response, item)
        return item

    def get_title(self, response, item):
        title = response.xpath("/html/head/title/text()").extract()
        if title:
            item['title'] = title[0][:-5]
#            zh_print(item['title'])

    def get_editor(self, response, item):
        editor= response.xpath("//span[@class='ep-editor']/text()").extract()
        if editor:
            item['editor'] = editor[0][5:-7]
#            zh_print(item['editor'])

    def get_source(self, response, item):
        source = response.xpath('//span[@class="left"]/text()').extract()
        if source:
            item['source'] = source[0][6:]
#            zh_print(item['source'])

    def get_date(self, response, item):
        date_source = response.xpath("//div[@class='post_time_source']/text()").extract()
        date = date_source[0].strip('\n').strip().split()[0].split('-')#remove \n and space
        if date:
            item['year'] = date[0]
            item['month'] = date[1]
            item['day'] = date[2]

    def get_passage(self, response, item):
        passage = response.xpath("//div[@class='post_text']/p/text()").extract()
        if passage:
            item['passage'] = "".join(passage)

def zh_print(ss):
    for s in ss:
        print s.encode("GBK");
    return
