from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
import logging
from ..items import ZillowItem
from scrapy.http import Request, HtmlResponse

logger = logging.getLogger('mycustomlogger')

class ZillowSpider(CrawlSpider) : 
    name = "zillow"
    allowed_domains = ["zillow.com"]
    start_urls = ["http://www.zillow.com/homes/recently_sold/Sunnyvale-CA-94086/house_type/97548_rid/any_days/37.448798,-121.978326,37.289999,-122.068449_rect/13_zm/"]
    rules = (
#        Rule(LinkExtractor(allow=(), allow_domains=('zillow.com'),restrict_xpaths=('//a[@class="off"]/@href',)), callback="parse_items", follow= True),
        Rule(LinkExtractor(allow=(), allow_domains=('zillow.com'),restrict_xpaths=('//a[@class="off"]',)), callback="parse_items", follow= True),
    )
#    def parse(self, response):
#        hxs = HtmlXPathSelector(response)
#        self.parse_items(response)
#        logger.info("Next URL is www.zillow.com%s", str(hxs.xpath('//a[@class="off"]/@href').extract()).strip('u\'[]'))
#        domain_name = "www.zillow.com"
#        url = domain_name+str(hxs.xpath('//a[@class="off"]/@href').extract()).strip('u\'[]')
#        logger.info("Next URL is: %s", url)


    def parse_items(self, response):
        logger.info("RESPONSE URL: %s", response.url)
        extract_url = LinkExtractor(allow=(), allow_domains=('zillow.com'),restrict_xpaths=('//a[@class="off"]',)).extract_links(response)
        logger.info("XXXXXXXXXXX extracted URL: %s", extract_url)
        hxs = HtmlXPathSelector(response)
        contents = hxs.xpath('//dt[@class="property-address"]//a')
        items =[]
        domain_name = "http://www.zillow.com"
        url = domain_name+str(hxs.xpath('//a[@class="off"]/@href').extract()).strip('u\'[]')
        for content in contents:
            item = ZillowItem()
            item["addr"] = content.xpath('span[@itemprop="streetAddress"]/text()').extract()
            item["city"] = content.xpath('span[@itemprop="addressLocality"]/text()').extract()
            item["state"] = content.xpath('span[@itemprop="addressRegion"]/text()').extract()
            item["zip"] = content.xpath('span[@itemprop="postalCode"]/text()').extract()
            item["url"] = content.xpath('@href').extract()
            logger.info("Addr %s", item['addr'])
            items.append(item)
        return (items)
