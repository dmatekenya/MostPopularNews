# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy
import sys
sys.path.insert(1,'/Users/dmatekenya/PycharmProjects/WebMining/')
from scrapy.item import Item, Field

class MostpopularnewsItem(scrapy.Item):
    title = Field()
    link = Field()
    desc = Field()
