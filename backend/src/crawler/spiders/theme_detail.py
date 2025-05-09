from bs4 import BeautifulSoup
import scrapy

from src.crawler.items import ThemeDetailItem
from src.crawler.database.models import NaverThemeListOrm
from src.crawler.database.session import SessionLocal


def generate_board_full_url(board_url):
    return f"https://finance.naver.com{board_url}"

class ThemeDetailSpider(scrapy.Spider):
    name = "theme_detail"
    allowed_domains = ["finance.naver.com"]
    start_urls = ["https://finance.naver.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "tg_crawler.pipelines.TgCrawlerThemeDetailPipeline": 1,
        }
    }

    def start_requests(self):
        session = SessionLocal()
        theme_list = session.query(NaverThemeListOrm).all()
        for theme in theme_list:
            yield scrapy.Request(
                theme.url, 
                callback=self.parse,
                meta={
                    "theme_name": theme.name,
                }
            )

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        names = []
        for name_area in soup.find_all("td", class_='name'):
            names.append(name_area.find("a").text)
        board_urls = []
        for board_url_area in soup.find_all("td", class_='center'):
            board_urls.append(board_url_area.find("a").get("href"))
        
        for name, board_url in zip(names, board_urls):
            yield ThemeDetailItem(
                theme_name=response.meta["theme_name"],
                stock_name=name,
                discussion_url=generate_board_full_url(board_url),
            )
