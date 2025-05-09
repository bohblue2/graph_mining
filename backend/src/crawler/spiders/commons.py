

import re
from urllib.parse import urlparse

import httpx

from src.crawler.items import NaverReportItem


def parse_report_url(url):
    """
    Parses a report URL and extracts relevant information.

    Args:
        url (str): The URL of the report.

    Returns:
        dict: A dictionary containing extracted information from the URL.
              Returns None if the URL doesn't match the expected pattern.

    Example:
        >>> url = "http://stock.pstatic.net/stock-research/market/64/20241014_market_675091000.pdf"
        >>> parse_report_url(url)
        {
            "category": "market",
            "company_id": "64",
            "date": "20241014",
            "report_type": "market",
            "report_id": "675091000"
        }
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    pattern = r"/stock-research/(\w+)/(\d+)/(\d{8})_(\w+)_(\d+)\.pdf"
    match = re.search(pattern, path)
    
    if match:
        category, company_id, date, report_type, report_id = match.groups()
        
        return NaverReportItem(
            category=category,
            security_company_id=company_id,
            date=date,
            report_type=report_type,
            report_id=report_id
        )
    else:
        return None

async def async_load_to_buffer(url: str, buffer: bytearray) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        
        if response.status_code == 200:
            buffer.extend(response.content)
            print("Buffer successfully loaded with data from the URL.")
        else:
            print(f"Failed to load buffer. Status code: {response.status_code}")