import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


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
        if len(response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[4]/text()')) > 2:
            item['timeM'] = int(response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[4]/text()')[0].extract()) * 60 + int(response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[4]/text()')[3].extract())
        else:
            item['timeM'] = int(response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[4]/text()')[0].extract())
        return item
