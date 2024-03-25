import scrapy
from OpenCritic.items import OpencriticItem 

class GamespiderSpider(scrapy.Spider):
    name = "gamespider"
    allowed_domains = ["opencritic.com"]
    start_urls = ["https://opencritic.com/browse/all?page=1"]
    page = 1
    max = 763

    def parse(self, response):
        # gets all the games
        games = response.css('div.game-name a')
        for game in games:
            relative_url = game.css('::attr(href)').get()
            if relative_url is not None:
                yield response.follow(relative_url, callback=self.parse_game_page)
        
        self.page += 1
        next_page = "https://opencritic.com/browse/all?page=" + str(self.page)
        
        if self.page <= self.max:
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse) 
    
    def parse_game_page(self, response):
        # Find all review blocks
        # review_names = response.css('.col-lg-5 div:nth-child(1)::text').getall()
        # review_scores = response.css('.col-lg-5 div .score-bold::text').getall()

        # reviews = {name.strip(): score.strip() for name, score in zip(review_names, review_scores)}

        game_item = OpencriticItem()
        game_item['OpenCritic_Rating'] = response.css('.col-4 img::attr(alt)').get()
        game_item['TopCritic_Average'] = response.css('.inner-orb::text').getall()[0]

        inner_orb_texts = response.css('.inner-orb::text').getall()
        if len(inner_orb_texts) > 1:
            game_item['Critics_Recommend'] = inner_orb_texts[1]
        else:
            game_item['Critics_Recommend'] = None

        # game_item['Critics_Recommend'] = response.css('.inner-orb::text').getall()[1]
        game_item['title'] = response.css('.mb-0::text').get()
        game_item['publisher'] = response.css('.companies span::text').get()
        game_item['platform'] = response.css('.platforms span strong::text').getall()
        game_item['date'] = response.css('.platforms::text').get()
        # game_item["reviews"] = reviews
        yield game_item
        # total 8025 scarpped 7341
#
#'Eurogamer': response.css('.col-lg-5 div .score-bold::text').getall()[0],
#'IGN': response.css('.col-lg-5 div .score-bold::text').getall()[1],
#'Easy_Allies': response.css('.col-lg-5 div .score-bold::text').getall()[2],
#'GamesRadar+': response.css('.col-lg-5 div .score-bold::text').getall()[3],
#'Metro_GameCentral': response.css('.col-lg-5 div .score-bold::text').getall()[4],
#'Game_Informer ': response.css('.col-lg-5 div .score-bold::text').getall()[5],
#'Polygon': response.css('.col-lg-5 div .score-bold::text').getall()[6],
#'GameSpot': response.css('.col-lg-5 div .score-bold::text').getall()[7],


# next page
#next_page = response.css('a[rel="next"]::attr(href)').get()
#if next_page is not None:
#    next_page = response.urljoin(next_page)
#    yield scrapy.Request(next_page, callback=self.parse)
# response.css('a[rel="next"]::attr(href)').get()
