import scrapy
import json
from Steam.items import SteamItem
import time


class PricespiderSpider(scrapy.Spider):
    name = "pricespider"
    allowed_domains = ["store.steampowered.com"]
    start_urls = ["https://store.steampowered.com/search/?sort_by=&sort_order=0&supportedlang=english&page=1"]

    def parse(self, response):
        current_page_number = response.meta.get('page', 1)
        
        #2/4/24
        # Next page number is current page plus one
        next_page_number = current_page_number + 1


        games = response.xpath('//*[@class="responsive_search_name_combined"]')
        for game in games:
             # First attempt to get the regular price
            price = game.xpath('.//*[@class="discount_original_price"]/text()').get()
            
            # If regular price is None, try to get the discounted price
            if price is None:
                price = game.xpath('.//*[@class="discount_final_price"]/text()').get()  
                # If discounted price is also None, try to get the 'free' price tag
                if price is None:
                    price = game.xpath('.//*[@class="discount_final_price free"]/text()').get()
            #gets app id for response.xpath('//a[@class="search_result_row ds_collapse_flag "]/@data-ds-appid').get()
            app_id = game.xpath('.//../@data-ds-appid').get()
            steam_request =  f"https://store.steampowered.com/appreviews/{app_id}?json=1"
            price_item = SteamItem()
            price_item['name'] = game.xpath('.//*[@class="col search_name ellipsis"]/span/text()').get()
            price_item['date'] = game.xpath('.//*[@class = "col search_released responsive_secondrow"]/text()').get()
            price_item['price'] = price
            # item = {
            #     'name': game.xpath('.//*[@class="col search_name ellipsis"]/span/text()').get(),
            #     'date': game.xpath('.//*[@class = "col search_released responsive_secondrow"]/text()').get(),
            #     'price': price,
            # }
        
            # Pass the item as meta data to the parse_reviews method
            #adds review to price item
            yield response.follow(steam_request, callback=self.parse_reviews, meta={'item': price_item})        
        next_page = f"https://store.steampowered.com/search/?sort_by=&sort_order=0&supportedlang=english&page={next_page_number}"
        
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse, meta={'page': next_page_number})
    
    def parse_reviews(self, response):
         # Convert the JSON response to a Python dictionary
        data = json.loads(response.text)
        
        # Now you can access total_positive and total_negative like so:
        total_positive = data.get('query_summary', {}).get('total_positive')
        total_negative = data.get('query_summary', {}).get('total_negative')
        total_reviews = data.get('query_summary', {}).get('total_reviews')

        review_score = data.get('query_summary', {}).get('review_score')
        review_score_desc = data.get('query_summary', {}).get('review_score_desc')

        # To pass these values back to the parse method, you can use the meta parameter
        # when yielding the request in your parse method like so:
        # yield response.follow(steam_request, callback=self.parse_reviews, meta={'item': item})
        # Here item would be the item you are yielding in the parse method.

        # Now you can include these values in your yield statement.
        # Assuming you have passed the original item as part of the meta
        item = response.meta.get('item', {})
        item['total_positive'] = total_positive
        item['total_negative'] = total_negative
        item['total_reviews'] = total_reviews
        item['review_score'] = review_score
        item['review_score_desc'] = review_score_desc
        yield item