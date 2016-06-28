from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
import logging
from ..items import ZillowItem
from ..items import ZillowItemDetail
from ..items import ZillowZid
from scrapy.http import Request, HtmlResponse

logger = logging.getLogger('mycustomlogger')

class ZillowSpider(CrawlSpider) : 
    name = "zillow_url"
    allowed_domains = ["zillow.com"]
#    start_urls = ["http://www.zillow.com/homes/recently_sold/Palo-Alto-CA-94306/house_type/97696_rid/any_days/37.456191,-122.040682,37.370975,-122.220927_rect/12_zm/"]
    start_urls = ["http://www.zillow.com/homes/recently_sold/Sunol-CA-94539/house_type/97746_rid/any_days/37.606616,-121.712895,37.444608,-122.073384_rect/11_zm/"]
    rules = (
        Rule(LinkExtractor(allow=(), allow_domains=('zillow.com'),restrict_xpaths=('//a[@class="off"]',)), callback="parse_items", follow= True),
        Rule(LinkExtractor(allow=(), allow_domains=('zillow.com'),restrict_xpaths=('//a[@class="on"]',)), callback="parse_items", follow= True),
    )

    def parse_start_url(self, response):
        return self.parse_items(response)

    def parse_items(self, response):
        logger.info("RESPONSE URL: %s", response.url)
        extract_url_off = LinkExtractor(allow=(), allow_domains=('zillow.com'),restrict_xpaths=('//a[@class="off"]',)).extract_links(response)
        extract_url_on = LinkExtractor(allow=(), allow_domains=('zillow.com'),restrict_xpaths=('//a[@class="on"]',)).extract_links(response)
        logger.info("XXXXXXXXXXX extracted OFF URL: %s", extract_url_off)
        logger.info("XXXXXXXXXXX extracted ON URL: %s", extract_url_on)
        return self.extract_summary(response)
 
    def extract_summary(self, response):
        logger.info("Start retrieve summary")
        hxs = HtmlXPathSelector(response)
        content = hxs.xpath('//ul[@class="photo-cards"]')
        url = hxs.xpath('//a[@class="zsg-photo-card-overlay-link routable hdp-link routable mask hdp-link"]/@href')
        items = []
        zid = content.xpath('//li//article/@data-zpid')
        longitude = content.xpath('//li//article/@data-longitude')
        latitude = content.xpath('//li//article/@data-latitude')
        for i in range(len(zid)):
            item = ZillowZid()
            item["zid"] = zid[i].extract()
            item["longitude"] = longitude[i].extract()
            item["latitude"] = latitude[i].extract()
            item["url"] = url[i].extract()
            items.append(item)
        return items
