# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from MostPopularNews.items import MostpopularnewsItem
from MostPopularNews.spiders import nyasa_spider

class MostpopularnewsPipeline(object):
    def process_item(self, item, spider):
        return item
