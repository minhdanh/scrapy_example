# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CustomerItem(scrapy.Item):
    id = scrapy.Field()
    firstname = scrapy.Field()
    lastname = scrapy.Field()
    phone = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
    state = scrapy.Field()

class CategoryItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
