from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
#from scrapy import ZillowItem 
import logging
from ..items import ZillowItem

logger = logging.getLogger('mycustomlogger')

class ZillowSpider(CrawlSpider) : 
    name = "zillow_simple"
    allowed_domains = ["zillow.com"]
    start_urls = ["http://www.zillow.com/homes/recently_sold/Sunnyvale-CA-94086/house_type/97548_rid/any_days/37.448798,-121.978326,37.289999,-122.068449_rect/13_zm/"]
    rules = (
#        Rule(LinkExtractor(allow=(), allow_domains=('zillow.com', ''),restrict_xpaths=('//a[@class="off"]/@href',)), callback="parse_items", follow= True),
        Rule(LinkExtractor(allow=(), allow_domains=('zillow.com'), restrict_xpaths=('//a[@class="off"]',)),callback='parse_obj', follow=True), 
    )
#    def parse(self, response):
#        logger.info("RESPONSE URL %s", response.url)
#        self.parse_items(response)

#    def parse_items(self, response):
#        logger.info("RESPONSE URL(items) %s", response.url)
    def parse_obj(self,response):
        logger.info("HIT XXXXXXXXXXX")
        for link in LinkExtractor(allow=(), restrict_xpaths=('//a[@class="off"]/@href',)).extract_links(response):
            logger.info("HIT YYYYYYYYYY")
            logger.info("LINK: %s", link.url)
