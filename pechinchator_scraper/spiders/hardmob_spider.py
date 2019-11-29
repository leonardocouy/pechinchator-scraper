import re
import cloudscraper
import scrapy
from pechinchator_scraper.items.thread_item import ThreadItem
from pechinchator_scraper.spiders.base_thread_spider import BaseThreadSpider
THREAD_VISITS_REGEX_PATTERN = r"\d+.*"
HARDMOB_BASE_URL = "https://www.hardmob.com.br/{}"

class HardmobSpider(BaseThreadSpider):
    name = "hardmob"
    allowed_domains = ["www.hardmob.com.br"]
    start_urls = ["https://www.hardmob.com.br/forums/407-Promocoes"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start_requests(self):
        cf_requests = []
        for url in self.start_urls:
            token, agent = cloudscraper.get_tokens(url)
            cf_requests.append(scrapy.Request(url=url,
                                              cookies=token,
                                              meta={"token": token, "agent": agent},
                                              headers={'User-Agent': agent}))
        return cf_requests

    def parse(self, response):
        thread_block_selectors = response.css("ol#threads > .threadbit")
        for thread_block in thread_block_selectors:
            thread = ThreadItem()
            thread_id = thread_block.css("li::attr(id)").extract_first()
            url = HARDMOB_BASE_URL.format(
                thread_block.css("a.title::attr(href)").extract_first()
            )
            title = thread_block.css("a.title::text").extract_first()
            posted_at = None

            stats_block = thread_block.css("ul.threadstats > li:not(.hidden)")

            replies = stats_block.css(".understate::text").extract_first()
            visits = stats_block.css("li:not(.hidden)::text").extract()[1]
            visits = re.search(THREAD_VISITS_REGEX_PATTERN, visits).group()

            thread.update({
                "url": url,
                "title": title,
                "posted_at": posted_at,
                "replies_count": replies,
                "visits_count": visits,
                "thread_id": thread_id.strip("thread_"),
                "source_id": self.name,
            })

            yield scrapy.Request(url=url,
              cookies=response.meta["token"],
              headers={'User-Agent': response.meta["agent"]},
              callback=self.parse_thread_content,
              meta={"thread": thread}
            )

    def parse_thread_content(self, response):
        thread = response.meta["thread"]
        details_block = response.css(".postdetails")
        thread["content_html"] = details_block.css(".postcontent").extract_first()
        thread["posted_at"] = " ".join([
            response.css(".date::text").extract_first().strip(),
            response.css(".date > .time::text").extract_first(),
        ])
        thread["offer_url"] = details_block.css(".postcontent > a::attr(href)").extract_first()
        yield thread
