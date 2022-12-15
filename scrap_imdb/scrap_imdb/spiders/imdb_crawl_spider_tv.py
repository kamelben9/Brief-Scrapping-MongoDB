import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re


class ImdbCrawlSpiderSpider(CrawlSpider):
    name = 'imdb_crawl_spider_tv'
    allowed_domains = ['www.imdb.com']
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250', headers={
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
        item['title'] = response.xpath('//h1/text()').get()
        item['original_title']= response.xpath('//div[@class="sc-dae4a1bc-0 gwBsXc"]/text()').get()
        item['score']= response.xpath('//span[@class="sc-7ab21ed2-1 jGRxWM"]/text()').get()
        item['genre']= response.xpath('//span[@class="ipc-chip__text"]/text()').getall()
        item['date']= response.xpath('//a[@class="ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh"]/text()').get()
        item['synopsis']=response.xpath('//span[@class="sc-16ede01-1 kgphFu"]/text()').get()
        duration = response.xpath('//ul[@data-testid="hero-title-block__metadata"]/*[last()]/text()').extract()
        if duration == []:
                item['durée'] = 0
        elif len(duration)== 5  :
            item['durée'] = int(duration[0]) * 60 + int(duration[3])
        elif len(duration) == 2 :
            if(duration[1]=="h"):
                item['durée'] =  int(duration[0]) * 60 
            else:
                item['durée'] =  int(duration[0])
        item['pays_origine'] = response.xpath('//section/div/ul/li[@class = "ipc-metadata-list__item"][1]/div[@class = "ipc-metadata-list-item__content-container"]/ul/li/a[@class = "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]/text()').getall()
        return item
