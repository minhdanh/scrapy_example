# -*- coding: utf-8 -*-

# Scrapy settings for scrapy_example_com project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'scrapy_example_com'

SPIDER_MODULES = ['scrapy_example_com.spiders']
NEWSPIDER_MODULE = 'scrapy_example_com.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'scrapy_example_com (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
  'scrapy_example_com.pipelines.ScrapyExampleComPipeline': 300
}
