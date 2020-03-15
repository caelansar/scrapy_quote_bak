# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class QuoteSpider(scrapy.Spider):
    name = 'quote'
    start_urls = ['http://quotes.toscrape.com/js/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, args={'images': 0})

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@class="author"]/text()').extract_first()
            yield {
                'text': text,
                'author': author,
            }
        next_page = response.xpath('//a[contains(text(),"Next")]/@href').extract_first()
        if next_page:
            absolute_url = response.urljoin(next_page)
            yield SplashRequest(absolute_url, args={'images': 0})
