from bs4 import BeautifulSoup
import scrapy

from src.crawler.items import NaverThemeDetailItem
from src.database.models.naver_theme import NaverThemeListOrm
from src.database.session import SessionLocal


def generate_board_full_url(board_url):
    return f"https://finance.naver.com{board_url}"

class NaverThemeDetailSpider(scrapy.Spider):
    name = "naver_theme_detail"
    allowed_domains = ["finance.naver.com"]
    start_urls = ["https://finance.naver.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            "src.crawler.pipelines.NaverThemeDetailPipeline": 1,
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
            yield NaverThemeDetailItem(
                theme_name=response.meta["theme_name"],
                stock_name=name,
                discussion_url=generate_board_full_url(board_url),
            )
