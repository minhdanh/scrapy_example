# -*- coding: utf-8 -*-
import scrapy
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy import log
from scrapy.http            import Request
from scrapy.selector        import Selector
from scrapy.contrib.loader  import XPathItemLoader
from urlparse               import urlsplit
from scrapy_example_com.items   import *
from datetime               import datetime


class ExampleSpiderSpider(scrapy.Spider):
    name = "example_spider"
    allowed_domains = ["17d8a6b3.ngrok.io"]
    start_urls = (
        'http://17d8a6b3.ngrok.io/users/sign_in',
    )

    def parse(self, response):
        ''' This is to refer to the base URL later '''
        global baseURL
        baseURL = urlsplit(response.url)[0] + '://' + urlsplit(response.url)[1];

        return scrapy.FormRequest.from_response(
            response,
            formdata={'user[email]': 'example@email.com', 'user[password]': 'samplepassword'},
            callback=self.after_login)

    def after_login(self, response):
      if "Invalid email or password" in response.body:
        self.log("Login failed", level=log.ERROR)
        return
      else:
        self.log("Logged in successful", level=log.INFO)
        yield Request(baseURL + '/customers', callback=self.get_customer_links)
        yield Request(baseURL + '/categories', callback=self.get_categories)
        return

    def get_customer_links(self, response):
      rows = response.xpath('/html/body/div[2]/div/div/div/table/tbody/tr')
      if len(rows) > 0:
        for row in rows:
          state = row.xpath('./td[5]/text()').extract()[0]
          link = row.xpath('./td[1]/a/@href').extract()[0]
          if re.match('/customers/\d+', link):
            yield Request(baseURL + link, callback=self.parse_customers, meta={'state': state})
      return

    def parse_customers(self, response):
      self.log("Parsing cusomers...", level=log.INFO)
      item = CustomerItem()
      item['state'] = self.translate_state(response.meta['state'])
      item['id'] = str(re.findall(r'\d+$', response.url)[0])
      firstname = response.xpath('/html/body/div[2]/div/div/dl[1]/dd[1]/text()').extract()
      item['firstname'] = firstname[0] if len(firstname) > 0 else None
      lastname = response.xpath('/html/body/div[2]/div/div/dl[1]/dd[2]/text()').extract()
      item['lastname'] = (lastname[0] if len(lastname) > 0 else None)
      phone = response.xpath('/html/body/div[2]/div/div/dl[1]/dd[3]/text()').extract()
      item['phone'] = (phone[0] if len(phone) > 0 else None)
      created_at = response.xpath('/html/body/div[2]/div/div/dl[1]/dd[6]/text()').extract() 
      created_at = str(datetime.strptime(created_at[0], '%d/%m/%Y %H:%M:%S'))
      item['created_at'] = created_at
      item['updated_at'] = created_at
      
      yield item
      
      return

    def get_categories(self, response):
      rows = response.xpath('/html/body/div[2]/div/div/div/table/tbody/tr')
      if len(rows) > 0:
        for row in rows:
          item = CategoryItem()
          item['id'] = row.xpath('./td[1]/text()').extract()[0]
          item['name'] = row.xpath('./td[2]/text()').extract()[0]
          yield item
          
      return

    def translate_state(self, state):
      state_dicts = {'unactivated': 0, 'activated': 1, 'banned': 10, 'unregistered': 11}
      return state_dicts[state]

