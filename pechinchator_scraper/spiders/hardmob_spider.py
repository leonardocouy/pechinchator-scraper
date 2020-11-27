import re
from scrapy_twitter import TwitterUserTimelineRequest, to_item
from dateutil.parser import parse as date_parse

from pechinchator_scraper.items.thread_item import ThreadItem
from pechinchator_scraper.spiders.base_thread_spider import BaseThreadSpider
THREAD_VISITS_REGEX_PATTERN = r"\d+.*"
THREAD_ID_REGEX_PATTERN = r"(?<=threads\/).+?(?=\-)"
HARDMOB_BASE_URL = "https://www.hardmob.com.br/{}"

class HardmobSpider(BaseThreadSpider):
    name = "hardmob"

    def __init__(self, *args, **kwargs):
        super(HardmobSpider, self).__init__(*args, **kwargs)
        self.screen_name = "hardmob_promo"
        self.count = 100

    def start_requests(self):
        return [
            TwitterUserTimelineRequest(
            screen_name = self.screen_name,
            count = 20)
        ]

    def parse(self, response):
        thread = ThreadItem()
        tweets = response.tweets[0:20]

        for tweet in tweets:
            parsed_tweet = to_item(tweet)
            title = re.sub(r'https?:\/\/.*[\r\n]*', '', parsed_tweet["text"], flags=re.MULTILINE).strip()
            posted_at = date_parse(parsed_tweet["created_at"])
            url = parsed_tweet["urls"][0]["expanded_url"]
            thread_id = re.search(THREAD_ID_REGEX_PATTERN, url).group()
            replies = 0
            visits = 0

            thread.update({
                "url": url,
                "title": title,
                "posted_at": posted_at,
                "replies_count": replies,
                "visits_count": visits,
                "content_html": parsed_tweet["text"],
                "thread_id": thread_id,
                "source_id": self.name,
            })
            yield thread