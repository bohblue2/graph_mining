# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ThemeListItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

class ThemeDetailItem(scrapy.Item):
    theme_name = scrapy.Field()
    stock_name = scrapy.Field()
    discussion_url = scrapy.Field()
