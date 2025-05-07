# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from tg_crawler.database.models import NaverThemeListOrm, NaverThemeDetailOrm
from tg_crawler.database.session import SessionLocal


class TgCrawlerPipeline:
    def process_item(self, item, spider):
        return item

class TgCrawlerThemeListPipeline:
    def open_spider(self, spider): 
        self.sess = SessionLocal()   
        
    def close_spider(self, spider): 
        self.sess.close()
        
    def process_item(self, item, spider):
        self.sess.add(NaverThemeListOrm(name=item['name'], url=item['url']))
        self.sess.commit()
        return item

class TgCrawlerThemeDetailPipeline:
    def open_spider(self, spider):
        self.sess = SessionLocal()
        
    def close_spider(self, spider):
        self.sess.close()
        
    def process_item(self, item, spider):
        self.sess.add(NaverThemeDetailOrm(
            theme_name=item['theme_name'],
            stock_name=item['stock_name'],
            discussion_url=item['discussion_url'],
        ))
        self.sess.commit()
        return item