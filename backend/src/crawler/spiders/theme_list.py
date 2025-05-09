import os
from bs4 import BeautifulSoup
import scrapy

from src.crawler.items import ThemeListItem

def generate_full_url(url: str) -> str:
    return f"https://finance.naver.com{url}"

class ThemeListSpider(scrapy.Spider):
    name = "theme_list"
    allowed_domains = ["finance.naver.com"]
    start_urls = [f"https://finance.naver.com/sise/theme.naver?&page={page}" for page in range(1, 10)]
    custom_settings = {
        "ITEM_PIPELINES": {
            "tg_crawler.pipelines.TgCrawlerThemeListPipeline": 1,
        }
    }

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        td_elements = soup.find_all("td", class_="col_type1")
        for td_element in td_elements:
            a_element = td_element.find("a")
            if a_element:
                theme_name = a_element.text
                theme_url = a_element.get("href", None)
                yield ThemeListItem(name=theme_name, url=generate_full_url(theme_url))

        if td_elements is None:
            return

