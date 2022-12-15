import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider, Rule


class ImdbSpider(Spider):
    name = 'spider_test'
    allowed_domains = ['www.imdb.com']
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'
    #url = "https://www.imdb.com/title/tt0903747/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=12230b0e-0e00-43ed-9e59-8d5353703cce&pf_rd_r=AWNVACHGCQQNWSW3Z8SG&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=toptv&ref_=chttvtp_tt_2"
    url = "https://www.imdb.com/title/tt5491994/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=12230b0e-0e00-43ed-9e59-8d5353703cce&pf_rd_r=HT10GRVFRPKFPBNF47A2&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i=toptv&ref_=chttvtp_tt_1"
    def start_requests(self):
        yield scrapy.Request(url=self.url, headers={
            'User-Agent': self.user_agent}, callback=self.parse_item
        )


    def parse_item(self, response):
        duree = response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[4]/text()').getall()
        duree = list(duree)

        if duree[1] == "h":
            int(response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[4]/text()')[0].extract()) * 60 + int(response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[4]/text()')[3].extract())
        else :
            response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[4]/text()').extract()
        
        print(duree)