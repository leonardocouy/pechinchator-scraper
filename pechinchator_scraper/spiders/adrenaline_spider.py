from pechinchator_scraper.items.thread_item import ThreadItem
from pechinchator_scraper.spiders.base_thread_spider import BaseThreadSpider
from scrapy.utils.project import get_project_settings
import time

settings = get_project_settings()

ADRENALINE_BASE_URL = "https://adrenaline.com.br{}"


class AdrenalineSpider(BaseThreadSpider):
    name = "adrenaline"
    allowed_domains = ["adrenaline.com.br"]
    start_urls = ["https://adrenaline.com.br/forum/forums/black-friday-2020/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, response):
        thread_block_selectors = response.css(".js-threadList .structItem--thread")

        for thread_block in thread_block_selectors:
            thread = ThreadItem()
            title_block = thread_block.css(".structItem-title")

            if len(thread_block.css(".structItem-status--locked")):
                continue

            url = ADRENALINE_BASE_URL.format(
                title_block.css("a::attr(href)").extract_first()
            ).strip("/unread").replace("uol.com.br", "com.br")
            title = title_block.css("a::text").extract_first()
            replies, visits = thread_block.css(".pairs.pairs--justified > dd::text").extract()

            thread.update({
                "url": url,
                "title": title,
                "replies_count": replies,
                "visits_count": visits,
                "source_id": self.name,
            })


            yield response.follow(
                url,
                callback=self.parse_thread_content,
                meta={"thread": thread}
            )

    def parse_thread_content(self, response):
        thread = response.meta["thread"]
        thread_date_epoch = response.css(".u-dt::attr(data-time)").extract_first()

        thread["thread_id"] = response.css("::attr(data-lb-id)").extract_first().strip("thread-")
        thread["posted_at"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(thread_date_epoch)))
        thread["content_html"] = response.css(
            ".lbContainer .js-lbContainer .bbWrapper"
        ).extract_first()
        thread["offer_url"] = response.css(".bbWrapper a::attr(href)").extract_first()

        yield thread
