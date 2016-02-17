# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ZillowItem(Item):
    # define the fields for your item here like:
    # name = Field()
    addr = Field()
    city = Field()
    state = Field()
    zip = Field()
    url = Field()
    pass
