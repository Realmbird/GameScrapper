import scrapy


class GamespiderSpider(scrapy.Spider):
    name = "gamespider"
    allowed_domains = ["opencritic.com"]
    start_urls = ["https://opencritic.com/browse/all?page=1"]

    def parse(self, response):
        # gets all the games
        games = response.css('div.game-name a')
        for game in games:
            relative_url = response.css('div.game-name a::attr(href)').get()
            if relative_url is not None:
                yield response.follow(relative_url, callback=self.parse_game_page)
            
        #next_page = response.css('a[rel="next"]::attr(href)').get()

        #if next_page is not None:
            #yield response.follow(next_page_url, callback=self.parse)
    
    def parse_game_page(self, response):
        yield {
            'OpenCritic_Rating': response.css('.col-4 img::attr(alt)').get(),
            'TopCritic_Average': response.css('.inner-orb::text').getall()[0],
            'Critics_Recommend': response.css('.inner-orb::text').getall()[1],
            'title': response.css('.mb-0::text').get(),
            'publisher': response.css('.companies span::text').get(),
            'date': response.css('.platforms span strong::text').get(),
        }

# next page
#next_page = response.css('a[rel="next"]::attr(href)').get()
#if next_page is not None:
#    next_page = response.urljoin(next_page)
#    yield scrapy.Request(next_page, callback=self.parse)
# response.css('a[rel="next"]::attr(href)').get()
