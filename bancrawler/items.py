# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class banned(scrapy.Item):
    username = scrapy.Field()
    duration = scrapy.Field()
    indefinitely = scrapy.Field()
    accumbans = scrapy.Field()

class exiled(scrapy.Item):
    exiledname = scrapy.Field()
    numoftoons = scrapy.Field()
    
class banner(scrapy.Item):
    username = scrapy.Field()
    accumdays = scrapy.Field()
    accuminds = scrapy.Field()
    accumbans = scrapy.Field()
