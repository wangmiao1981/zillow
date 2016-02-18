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
    sold_date = Field()
    price = Field()
    price_sqt = Field()
    beds = Field()
    lot = Field()
    built_year = Field()
    pass
