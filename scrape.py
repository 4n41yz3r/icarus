import scrapy

class RarbgSpider(scrapy.Spider):
    name = 'rarbgspider'
    start_urls = ['https://rarbg.to/torrents.php?category=movies']

    def parse(self, response):
        for title in response.css('td.lista'):
            yield { 'title': title.css('a ::text').extract_first() }
