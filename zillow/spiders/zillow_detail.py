from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
import logging
from ..items import ZillowItem
from ..items import ZillowItemDetail
from scrapy.http import Request, HtmlResponse

logger = logging.getLogger('mycustomlogger')

class ZillowSpider(CrawlSpider) : 
    name = "zillow_detail"
    allowed_domains = ["zillow.com"]
#    start_urls = ["http://www.zillow.com/homes/recently_sold/Sunnyvale-CA-94086/house_type/97548_rid/any_days/37.448798,-121.978326,37.289999,-122.068449_rect/13_zm/"]
#    start_urls = ["http://www.zillow.com/homes/recently_sold/Sunnyvale-CA-94087/house_type/97549_rid/any_days/37.395937,-121.940432,37.310652,-122.120677_rect/12_zm/"]
#    start_urls = ["http://www.zillow.com/homes/recently_sold/Santa-Clara-CA-95051/house_type/97952_rid/any_days/37.3943,-121.89477,37.309014,-122.075015_rect/12_zm/"]
#    start_urls = ["http://www.zillow.com/homes/recently_sold/Cupertino-CA-95014/house_type/97926_rid/any_days/37.383252,-121.892796,37.212558,-122.253285_rect/11_zm/"]
    start_urls = ["http://www.zillow.com/homes/recently_sold/Palo-Alto-CA-94306/house_type/97696_rid/any_days/37.456191,-122.040682,37.370975,-122.220927_rect/12_zm/"]
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
        content = hxs.xpath('//div[@class="property-listing-data"]')
        items = []
        addr_block = content.xpath('//dt[@class="property-address"]//a')
        sold_price = content.xpath('//dt[@class="listing-type zsg-content_collapsed"]/text()')
        price_sqt = content.xpath('//dt[@class="zsg-fineprint"]/text()')
        sold_date = content.xpath('//dt[@class="sold-date zsg-fineprint"]/text()')
        property_data = content.xpath('//dt[@class="property-data"]')
        domain_name = "http://www.zillow.com"
        for i in range(len(content)):
            item = ZillowItemDetail()
            url = domain_name + str(addr_block[i].xpath('@href').extract()).strip('u\'[]')
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
            yield Request(url, meta= {'item':item, 'items':items},callback=self.extract_details)
#            items.append(item)
#            logger.info("111111111111111111111: After Yeild")
#        return items

    def extract_details(self, response):
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        items = response.meta['items']
        item["facts"] = hxs.xpath('//ul[@class="zsg-list_square zsg-lg-1-3 zsg-md-1-2 zsg-sm-1-1"]/li/text()').extract()
        zest = hxs.xpath('//div[@class="zest-value"]/text()').extract()
        item["zest_sale"] = zest[0]
        item["zest_rent"] = zest[1]
        school_info = hxs.xpath('//ul[@class="nearby-schools-list"]')
        school_name = school_info.xpath('//a[@class="za-track-event school-name notranslate"]/text()').extract()
        school_rating = school_info.xpath('//span[@class="gs-rating-number gs-rating-10"]/text()').extract()
        school_grade = school_info.xpath('//div[@class="nearby-schools-grades"]/text()').extract()
        school_len = len(school_name)
        if school_len == 1:
            item["school_info1"] = str(school_name[0]) + "/" + str(school_rating[0]) + "/" + str(school_grade[0]) 
        elif school_len == 2:
            item["school_info1"] = str(school_name[0]) + "/" + str(school_rating[0]) + "/" + str(school_grade[0]) 
            item["school_info2"] = str(school_name[1]) + "/" + str(school_rating[1]) + "/" + str(school_grade[1]) 
        elif school_len == 3:
            item["school_info1"] = str(school_name[0]) + "/" + str(school_rating[0]) + "/" + str(school_grade[0]) 
            item["school_info2"] = str(school_name[1]) + "/" + str(school_rating[1]) + "/" + str(school_grade[1]) 
            item["school_info3"] = str(school_name[2]) + "/" + str(school_rating[2]) + "/" + str(school_grade[2]) 
        else:
            logger.info("No school info") 
        items.append(item)
        return items
