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
        Rule(LinkExtractor(allow=(), allow_domains=('zillow.com'),restrict_xpaths=('//a[@class="off"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        logger.info("RESPONSE URL: %s", response.url)
        extract_url = LinkExtractor(allow=(), allow_domains=('zillow.com'),restrict_xpaths=('//a[@class="off"]',)).extract_links(response)
        logger.info("XXXXXXXXXXX extracted URL: %s", extract_url)
        return self.extract_summary(response)
#        hxs = HtmlXPathSelector(response)
#        contents = hxs.xpath('//dt[@class="property-address"]//a')
#        items =[]
#        domain_name = "http://www.zillow.com"
#        url = domain_name+str(hxs.xpath('//a[@class="off"]/@href').extract()).strip('u\'[]')
#        for content in contents:
#            item = ZillowItem()
#            item["addr"] = content.xpath('span[@itemprop="streetAddress"]/text()').extract()
#            item["city"] = content.xpath('span[@itemprop="addressLocality"]/text()').extract()
#            item["state"] = content.xpath('span[@itemprop="addressRegion"]/text()').extract()
#            item["zip"] = content.xpath('span[@itemprop="postalCode"]/text()').extract()
#            item["url"] = content.xpath('@href').extract()
#            logger.info("Addr %s", item['addr'])
#            items.append(item)
#        return (items)
 
    def extract_summary(self, response):
        logger.info("Start retrieve summary")
        hxs = HtmlXPathSelector(response)
        content = hxs.xpath('//div[@class="property-listing-data"]')
        items = []
#        for content in contents:
        addr_block = content.xpath('//dt[@class="property-address"]//a')
        sold_price = content.xpath('//dt[@class="listing-type zsg-content_collapsed"]/text()')
        price_sqt = content.xpath('//dt[@class="zsg-fineprint"]/text()')
        sold_date = content.xpath('//dt[@class="sold-date zsg-fineprint"]/text()')
        property_data = content.xpath('//dt[@class="property-data"]')
        for i in range(len(addr_block)):
            item = ZillowItem()
            item["addr"] = addr_block[i].xpath('span[@itemprop="streetAddress"]/text()').extract()
            item["city"] = addr_block[i].xpath('span[@itemprop="addressLocality"]/text()').extract()
            item["state"] = addr_block[i].xpath('span[@itemprop="addressRegion"]/text()').extract()
            item["zip"] = addr_block[i].xpath('span[@itemprop="postalCode"]/text()').extract()
            item["url"] = addr_block[i].xpath('@href').extract()
            item["sold_date"] = sold_date[i].extract()
            item["price"] = sold_price[i].extract()
            item["price_sqt"] = price_sqt[i].extract()
            item["beds"] = property_data[i].xpath('span[@class="beds-baths-sqft"]/text()').extract()
            item["lot"] = property_data[i].xpath('span[@class="lot-size"]/text()').extract()
            item["built_year"] = property_data[i].xpath('span[@class="built-year"]/text()').extract()
            items.append(item)
        return items
