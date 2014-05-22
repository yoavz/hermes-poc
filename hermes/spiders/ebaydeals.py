import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from hermes.items import EbayItem

ID_RE = re.compile(r"http://www.ebay.com/itm/[^/]+/(\d+)")
PRICE_XPATH = r"//span[@id='prcIsum']/text()"
TITLE_XPATH = r"//h1[@id='itemTitle']/text()"

class EbaySpider(CrawlSpider):
    name = "ebay"
    allowed_domains = ["ebay.com"]
    start_urls = ["http://deals.ebay.com/tech-deals"]
    ebay_deals_url = r"http://deals.ebay.com/[^/]+$"
    deal_url = r"http://www.ebay.com/itm/[^/]+/(\d+)"
    rules = (
            # actually scrape a deal url
            Rule(SgmlLinkExtractor(allow=(ebay_deals_url, ))),

            # follow all other links
            Rule(SgmlLinkExtractor(allow=(deal_url, )), callback="parse_page"),
    )

    def parse_page(self, response):
        sel = Selector(response)
        item = EbayItem()

        item['url'] = str(response.url)
        title = sel.xpath(TITLE_XPATH).extract()[0].strip()
        item['title'] = title
        item['tags'] = [x.lower() for x in re.split('\W+', title)]
        item['price'] = sel.xpath(PRICE_XPATH).extract()[0].strip()
        if ID_RE.match(response.url):
            item['id'] = ID_RE.match(response.url).group(1)
        return item
