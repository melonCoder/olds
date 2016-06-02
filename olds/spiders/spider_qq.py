 # -*- coding: utf-8 -*-
import re
from scrapy.selector import Selector
from olds.items import OldsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime

class spider_qq(CrawlSpider):
    name = "spider_qq"
    allowed_domains = ["news.qq.com"]
    start_urls = ['http://news.qq.com']
    allowed_urls = datetime.datetime.now().strftime("/%Y%m%d/\d+")
    rules = (
        Rule(
            LinkExtractor(allow=re.compile(allowed_urls)),
            callback = "parse_item",
            follow = True ##whether to continue recursively
            ),
    )

    def parse_item(self, response):
        item = OldsItem()
        item['olds_thread'] = response.url.strip().split('/')[-1][:-4]
        item['source'] = "qq"
        self.get_title(response, item)
        self.get_editor(response, item)
        self.get_oriSource(response, item)
        self.get_date(response, item)
        self.get_passage(response, item)
        return item

    def get_title(self, response, item):
        title = response.xpath("/html/head/title/text()").extract()
        if title:
            item['title'] = title[0][:-7]

    def get_editor(self, response, item):
        editor= response.xpath("//*[@id='QQeditor']/text()").extract()
        if editor:
            item['editor'] = editor[0][6:-1]

    def get_oriSource(self, response, item):
        oriSource = response.xpath("//div[@id='C-Main-Article-QQ']//span[@bosszone='jgname']/a/text()").extract()
        if oriSource:
            item['oriSource'] = oriSource[0]

    def get_date(self, response, item):
        date_source = response.xpath("//span[@class='article-time']/text()").extract()
        if date_source:
            date = date_source[0].strip('\n').strip().split()[0].split('-')#remove \n and space
            item['year'] = date[0]
            item['month'] = date[1]
            item['day'] = date[2]

    def get_passage(self, response, item):
        passage = response.xpath("//*[@id='Cnt-Main-Article-QQ']/p/text()").extract()
        if passage:
            item['passage'] = "".join(passage)
