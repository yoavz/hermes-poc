import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector

from hermes.items import DealnewsItem

ID_RE = re.compile(r'http://dealnews.com/[^/]+/(\d+).html')
PRICE_XPATH = r"//div[contains(concat(' ', @class, ' '), 'price')]/text()"
PRODUCT_TITLE_XPATH = r"//h1[contains(concat(' ', @class, ' '), 'headline')]/a/text()"

class DealnewsSpider(CrawlSpider):
    name = "dealnews"
    allowed_domains = ["dealnews.com"]
    start_urls = ["http://dealnews.com/c39/Computers/"]
    computers = r"http://dealnews.com/[^/]+/Computers/.*"
    skip_these = r"http://dealnews.com/[^/]+/Computers/.*/\?"
    skip_these_also = r"http://dealnews.com/[^/]+/Computers/\?.*"
    deal_url = r"http://dealnews.com/[^/]+/\d+.html"
    rules = (
            # actually scrape a deal url
            Rule(SgmlLinkExtractor(allow=(computers, ), deny=(skip_these, skip_these_also))),

            # follow all other links
            Rule(SgmlLinkExtractor(allow=(deal_url, )), callback="parse_page"),
    )

    def parse_page(self, response):
        sel = Selector(response)
        item = DealnewsItem()

        item['url'] = str(response.url)
        product_title = sel.xpath(PRODUCT_TITLE_XPATH).extract()[0].strip()
        item['title'] = product_title
        item['tags'] = [x.lower() for x in re.split('\W+', product_title)]
        item['price'] = sel.xpath(PRICE_XPATH).extract()[0].strip()
        if ID_RE.match(response.url):
            item['id'] = ID_RE.match(response.url).group(1)
        return item
