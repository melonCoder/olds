 # -*- coding: utf-8 -*-
import re
from scrapy.selector import Selector
from olds.items import OldsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import datetime

class spider_sina(CrawlSpider):
    name = "spider_sina"
    allowed_domains = ["news.sina.com.cn"]
    start_urls = ['http://news.sina.com.cn']
    allowed_urls = datetime.datetime.now().strftime("/%Y-%m-%d/*")
    rules = (
        Rule(
            LinkExtractor(allow=re.compile(allowed_urls)),
            callback = "parse_item",
            follow = True ##whether to continue recursively
            ),
    )

    def parse_item(self, response):
        item = OldsItem()
        item['olds_thread'] = response.url.strip().split('/')[-1][:-6]
        item['source'] = "sina"
        self.get_title(response, item)
        self.get_editor(response, item)
        self.get_oriSource(response, item)
        self.get_date(response, item)
        self.get_passage(response, item)
        return item

    def get_title(self, response, item):
        title = response.xpath("/html/head/title/text()").extract()
        if title:
            item['title'] = title[0][:-5]

    def get_editor(self, response, item):
        editor= response.xpath("//p[@class='article-editor']/text()").extract()
        if editor:
            item['editor'] = editor[0][5:]

    def get_oriSource(self, response, item):
        oriSource = response.xpath('//span[@data-sudaclick="media_name"]/a/text()').extract()
        if oriSource:
            item['oriSource'] = oriSource[0]

    def get_date(self, response, item):
        date_source_tmp = response.xpath("//span[@id='navtimeSource']/text()").extract()
        if date_source_tmp:
            date_source = date_source_tmp
        else:
            date_source = response.xpath("//span[@id='pub_date']/text()").extract()
        if date_source:
            date = re.findall(r'\d+', date_source[0])
            item['year'] = date[0]
            item['month'] = date[1]
            item['day'] = date[2]

    def get_passage(self, response, item):
        passage = response.xpath("//div[@id='artibody']/p/text()").extract()
        if passage:
            item['passage'] = "".join(passage)
