import scrapy
import re
import math
import time

class SalesspiderSpider(scrapy.Spider):
    name = "salesspider"
    allowed_domains = ["vgchartz.com"]
    start_urls = ["https://www.vgchartz.com/games/games.php?page=1&results=200&name=&console=&keyword=&publisher=&genre=action&order=Sales&ownership=Both&boxart=Both&banner=Both&showdeleted=&region=All&goty_year=&developer=&direction=DESC&showtotalsales=1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher=1&showdeveloper=1&showreleasedate=1&showlastupdate=1&showvgchartzscore=1&showcriticscore=1&showuserscore=1&showshipped=1&alphasort=&showmultiplat=No"]

    page = 1 # The first page we will need to jump to is page number 2, so this is that variable
    genre = 0 # We are starting at the first genre in the list

    # genre list
    genre_list = ["Action",
             "Adventure",
             "Action-Adventure",
             "Board+Game",
             "Education",
             "Fighting",
             "Misc",
             "MMO",
             "Music",
             "Party",
             "Platform",
             "Puzzle",
             "Racing",
             "Role-Playing",
             "Sandbox",
             "Shooter",
             "Simulation",
             "Sports",
             "Strategy",
             "Visual+Novel"]

    def parse(self, response):

        for row in response.xpath('//*[@id="generalBody"]/table[1]/tr'):
            yield {
                'img' : row.xpath(".//td[2]/div/a/div/img/@src").get(),
                'title' : row.xpath(".//td[3]/a/text()").get(),
                'console' : row.xpath(".//td[4]/img/@alt").get(),
                'publisher' : row.xpath(".//td[5]/text()").get(),
                'developer' : row.xpath(".//td[6]/text()").get(),
                'vg_score' : row.xpath(".//td[7]/text()").get(),
                'critic_score' : row.xpath(".//td[8]/text()").get(),
                'user_score' : row.xpath(".//td[9]/text()").get(),
                'total_shipped' : row.xpath(".//td[10]/text()").get(),
                'total_sales' : row.xpath(".//td[11]/text()").get(),
                'na_sales' : row.xpath(".//td[12]/text()").get(),
                'pal_sales' : row.xpath(".//td[13]/text()").get(),
                'jp_sales' : row.xpath(".//td[14]/text()").get(),
                'other_sales' : row.xpath(".//td[15]/text()").get(),
                'release_date' : row.xpath(".//td[16]/text()").get(),
                'last_update' : row.xpath(".//td[17]/text()").get(),
                'genre' : self.genre_list[self.genre]
            }

        # next_page = response.xpath('//*[@id="generalBody"]/table[1]/tr/th[2]//span[2]/a/@href').get()
        # #turns relative to normal href
        # # page = 2 # The first page we will need to jump to is page number 2, so this is that variable
        # # genre = 0 # We are starting at the first genre in the list  
        # "https://www.vgchartz.com/games/games.php?page=1&results=200&name=&console=&keyword=&publisher=&genre=action&order=Sales&ownership=Both&boxart=Both&banner=Both&showdeleted=&region=All&goty_year=&developer=&direction=DESC&showtotalsales=1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher=1&showdeveloper=1&showreleasedate=1&showlastupdate=1&showvgchartzscore=1&showcriticscore=1&showuserscore=1&showshipped=1&alphasort=&showmultiplat=No"

        next_page = "https://www.vgchartz.com/games/games.php?page=" + str(self.page) + "&results=200&name=&console=&keyword=&publisher=&genre="+ self.genre_list[self.genre] + "&order=Sales&ownership=Both&boxart=Both&banner=Both&showdeleted=&region=All&goty_year=&developer=&direction=DESC&showtotalsales=1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher=1&showdeveloper=1&showreleasedate=1&showlastupdate=1&showvgchartzscore=1&showcriticscore=1&showuserscore=1&showshipped=1&alphasort=&showmultiplat=No"
        print(next_page)
        results = response.xpath('.//*[@id="generalBody"]/table[1]/tr[1]/th[1]/text()').get()
        results_pat = r'([0-9]{1,9})'
        results = results.replace(",", "")
        
        last_page = math.ceil(int(re.search(results_pat, results).group(1)) / 200)

        if (self.page > last_page) & (self.genre_list[self.genre] == "Visual+Novel"):
            print(self.genre_list[self.genre])
            return "All done!"

        # If we've reached the last page, but not the last genre (anything BUT Visual Novel), we'll reset our page, move onto the
        # next genre and keep scraping.
        elif (self.page > last_page) & (self.genre_list[self.genre] != "Visual+Novel"):
            print(self.genre_list[self.genre])
            self.page = 1
            self.genre += 1
            next_page = "https://www.vgchartz.com/games/games.php?page=" + str(self.page) + "&results=200&name=&console=&keyword=&publisher=&genre="+ self.genre_list[self.genre] + "&order=Sales&ownership=Both&boxart=Both&banner=Both&showdeleted=&region=All&goty_year=&developer=&direction=DESC&showtotalsales=1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher=1&showdeveloper=1&showreleasedate=1&showlastupdate=1&showvgchartzscore=1&showcriticscore=1&showuserscore=1&showshipped=1&alphasort=&showmultiplat=No"
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
                )
            self.page += 1

        # If we haven't reached the last page at all, we can just keep going without changing the genre parameter, we'll just have
        # to move onto the next page
        elif next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
                )
            time.sleep(3)
            self.page += 1


        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
            


        # # Select all the tr elements
        # tr_elements = response.css('table > tr')

        # # Filter out tr elements that contain th children
        # filtered_tr_elements = [tr for tr in tr_elements if not tr.css('th')]

        # # Get the HTML for each filtered tr element
        # filtered_tr_html = [tr.get() for tr in filtered_tr_elements]
        pass
