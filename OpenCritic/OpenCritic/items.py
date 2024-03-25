# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OpencriticItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    OpenCritic_Rating = scrapy.Field()
    TopCritic_Average = scrapy.Field()
    Critics_Recommend  = scrapy.Field()
    title = scrapy.Field()
    publisher  = scrapy.Field()
    platform = scrapy.Field()
    date = scrapy.Field()
    # reviews = scrapy.Field()
