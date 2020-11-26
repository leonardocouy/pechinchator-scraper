import re

from pechinchator_scraper.items.thread_item import ThreadItem
from pechinchator_scraper.spiders.base_thread_spider import BaseThreadSpider

THREAD_VISITS_REGEX_PATTERN = r"\d+.*"

PROMOBIT_BASE_URL = "https://www.promobit.com.br{}"


class PromobitSpider(BaseThreadSpider):
    name = "promobit"
    allowed_domains = ["www.promobit.com.br"]
    start_urls = ["https://www.promobit.com.br/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, response):
        thread_block_selectors = response.css(".timeline_content #offers .pr-tl-card")

        for thread_block in thread_block_selectors:
            thread = ThreadItem()
            thread_id = thread_block.css("::attr(data-key)").extract_first()
            url = PROMOBIT_BASE_URL.format(
                thread_block.css("a.access_url::attr(href)").extract_first()
            )
            price = "R$ " + thread_block.css("meta[itemprop='lowPrice']").xpath('@content').extract_first()
            title = thread_block.css("a.access_url::text").extract_first() + " - " + price
            posted_at = None

            replies = thread_block.css(".card-box.like .label::text").extract_first()
            visits = thread_block.css(".comments-box .label::text").extract_first()

            thread.update({
                "url": url,
                "title": title,
                "posted_at": posted_at,
                "replies_count": replies,
                "visits_count": visits,
                "thread_id": thread_id.strip("thread_"),
                "source_id": self.name,
            })

            yield response.follow(
                url,
                callback=self.parse_thread_content,
                meta={"thread": thread}
            )

    def parse_thread_content(self, response):
        thread = response.meta["thread"]

        details_block = response.css(".pr-of-info.prs-box")
        thread["content_html"] = details_block.css(".pr-of-info-container > *").extract_first()
        thread["posted_at"] = response.css("[itemprop='availabilityStarts']::attr(content)").extract_first()

        yield thread
