# -*- coding: utf-8 -*-
import scrapy
import urllib
import sys
from XoCrawler.items import XocrawlerItem


class XoSpider(scrapy.Spider):
    name = "Xo"
    allowed_domains = ["xo.gr"]
    # start_urls = (
    #     'https://www.xo.gr/dir-az/L/Logistika-Grafeia-Logistes/Kallithea%20Attikis/',
    # )

    def __init__(self, url='https://www.xo.gr/dir-az/L/Logistika-Grafeia-Logistes/Kallithea%20Attikis/', *args, **kwargs):
        super(XoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [ url ]

    # def __init__(self, what='', where=''):
    #     what = what.decode(sys.getfilesystemencoding()).encode('utf8')
    #     where = where.decode(sys.getfilesystemencoding()).encode('utf8')
    #
    #     urlencodedParams = urllib.urlencode({
    #         "what": what,
    #         "where": where
    #     })
    #     self.start_urls = ['http://www.xo.gr/search/?%s' % urlencodedParams]

    def parse(self, response):
        # print self.start_urls
        # print 'item'
        for doc in response.css('li.span12.listing'):
            item = XocrawlerItem()
            item['title'] = doc.css('.listingBusinessNameArea > h2 > a > span').xpath('text()').extract()[0]
            item['address'] = ''.join(doc.css(".listingAddressInfo > .address .addressProfile *::text").extract())
            item['tel'] = doc.css('.listingMainCallToActions > .listingPhones .dropdown-menu a').xpath('@href').extract()

            if not item['tel']:
                item['tel'] = ''
            else:
                item['tel'] = item['tel'][0]
                item['tel'] = item['tel'].split('tel:', 1)[1]

            item['email'] = doc.css('.listingEmail > a').xpath('@href').extract()
            if not item['email']:
                item['email'] = ''
            else:
                item['email'] = item['email'][0]
                item['email'] = item['email'][7:]
                item['email'] = item['email'].split('?', 1)[0]

            print 'item'

            yield item

        next_page = response.css(".pagination .page_next::attr('href')")
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)
