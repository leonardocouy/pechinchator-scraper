from pechinchator_scraper.items.thread_item import ThreadItem
from pechinchator_scraper.spiders.base_thread_spider import BaseThreadSpider

GATRY_BASE_URL = "https://gatry.com/{}"


class GatrySpider(BaseThreadSpider):
    name = "gatry"
    allowed_domains = ["gatry.com"]
    start_urls = ["https://gatry.com/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, response):
        thread_block_selectors = response.css(".promocao")

        for thread_block in thread_block_selectors:
            thread = ThreadItem()
            thread_id = thread_block.css(".promocao::attr(id)").extract_first()
            url = GATRY_BASE_URL.format(
                thread_block.css(".opcoes a.mais::attr(href)").extract_first()
            )
            price = "R$ " + thread_block.css("p.preco > [itemprop='price']::text").extract_first()
            title = thread_block.css("h3[itemprop='name'] > a::text").extract_first() + " - " + price
            posted_at = thread_block.css(".opcoes .data_postado::attr(title)").extract_first()

            replies = thread_block.css(".opcoes .link-comentarios::text").extract_first().strip()
            visits = thread_block.css(".opcoes .link-comentarios::text").extract_first().strip()

            thread.update({
                "url": url,
                "title": title,
                "posted_at": posted_at,
                "replies_count": replies,
                "visits_count": visits,
                "thread_id": thread_id.strip("promocao-"),
                "source_id": self.name,
            })

            yield response.follow(
                url,
                callback=self.parse_thread_content,
                meta={"thread": thread}
            )

    def parse_thread_content(self, response):
        thread = response.meta["thread"]

        image_url = response.css(".imagem img::attr(src)").extract_first()
        offer_url = response.css(".imagem a::attr(href)").extract_first()
        content = response.css(".content-comentario::text").extract_first()
        custom_html = """
        <p>
          <img src="{image_url}" align="middle" />
          {content}
          <br>
          <a href="{product_url}" target="_blank">
            Link
          </a>
        </p>
        """.format(image_url=image_url, content=content, product_url=offer_url)

        thread["content_html"] = custom_html
        yield thread
