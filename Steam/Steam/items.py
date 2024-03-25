# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    total_positive = scrapy.Field()
    total_negative = scrapy.Field()
    total_reviews = scrapy.Field()
    review_score = scrapy.Field()
    review_score_desc = scrapy.Field()

    #steam page goes to https://store.steampowered.com/appreviews/631920?json=1> (referer: https://store.steampowered.com/search/?sort_by=&sort_order=0&supportedlang=english&page=3522

    # query_summary - Returned in the first request

    # num_reviews - The number of reviews returned in this response
    # review_score - The review score
    # review_score_desc - The description of the review score
    # total_positive - Total number of positive reviews
    # total_negative - Total number of negative reviews
    # total_reviews - Total number of reviews matching the query parameters
