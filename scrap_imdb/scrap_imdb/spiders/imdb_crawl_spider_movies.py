import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ImdbCrawlSpiderSpider(CrawlSpider):
    name = 'imdb_crawl_spider'
    allowed_domains = ['www.imdb.com']
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/?ref_=nv_mv_250', headers={
            'User-Agent': self.user_agent
        })

    Le_imdb_details = LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a")
    rule_imdb_details = Rule(Le_imdb_details, 
                            callback='parse_item', 
                            follow=True)
    rules = (
        rule_imdb_details ,
    )

    def parse_item(self, response):
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        item['title'] = response.xpath('//h1/text()').get()
        item['original_title']= response.xpath('//div[@class="sc-dae4a1bc-0 gwBsXc"]/text()').get()
        item['date'] = response.xpath('(//span[@class="sc-8c396aa2-2 itZqyK"]/text())[1]').get()
        item['score'] = response.xpath('//span[@class = "sc-7ab21ed2-1 jGRxWM"]/text()').get()
        item['genre'] = response.xpath('//span[@class = "ipc-chip__text"]/text()[1]').get()
        item['durée'] = int(response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[3]/text()')[0].get())*60 + int(response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[3]/text()')[3].get())
        item['synopsis'] = response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/p/span[1]/text()').get()
        item['acteurs'] = response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul/li/a/text()').extract()
        item['public'] = response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[2]/a/text()').get()
        return item

