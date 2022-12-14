import scrapy


class ImdbSpiderSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ['imdb.com']
    start_urls = [
        'http://imdb.com/'
        'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    ]

    def parse(self, response):
        title = response.css('title').extract()
        yield {'Titre ': title}
