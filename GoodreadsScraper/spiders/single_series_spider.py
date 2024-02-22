"""Spider to extract URL's of books from a single author"""

import scrapy
from scrapy import signals
from .book_spider import BookSpider


class SingleSeriesSpider(scrapy.Spider):
    """Extract and crawl URLs of books from one of the "My Books" shelf for a user
        This subsequently passes on the URLs to BookSpider.
        Consequently, this spider also yields BookItem's and AuthorItem's.
    """
    name = "single-series"

    def _set_crawler(self, crawler):
        super()._set_crawler(crawler)
        crawler.signals.connect(self.item_scraped_callback,
                                signal=signals.item_scraped)

    def __init__(self, series_id, item_scraped_callback=None):
        super().__init__()
        self.book_spider = BookSpider()
        self.item_scraped_callback = item_scraped_callback
        self.start_urls = [ f"https://www.goodreads.com/series/{series_id}"]

    def parse(self, response):
        book_urls = response.css("div.responsiveBook__media a::attr(href)").extract()
        book_urls = ['https://goodreads.com' + i for i in book_urls]

        for book_url in book_urls:
            yield response.follow(book_url, callback=self.book_spider.parse)