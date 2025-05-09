from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import List
import datetime
from src.api.models import GraphResponse, QueryInfo, CompanyNode, KeywordNode, Edge # type: ignore

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)



@app.get("/")
async def root():
    return {"message": "Graph Mining API"}


@app.get("/test")
async def test():
    with open("graph_example.json", "r") as f:
        return json.load(f)

MOCK_COMPANIES: List[CompanyNode] = [
    CompanyNode(
        ISIN="US67066G1040",
        name="NVIDIA",
        priceFrom=113.54,
        priceTo=115.54,
        priceChange=1.0176149375,
        currency="USD",
        market="NASDAQ",
        source="Yahoo Finance",
    )
]

MOCK_KEYWORDS: List[KeywordNode] = [
    KeywordNode(keyword="AI 칩", priceChange=1.0176149375)
]

MOCK_EDGES: List[Edge] = [
    Edge(source="NVIDIA", target="AI 칩", weight=0.5)
]


@app.get("/graph", response_model=GraphResponse)
async def get_graph(from_date: str = "2024-01-01", to_date: str = "2024-01-02"):
    """Return mocked graph data for the requested date range.

    Args:
        from_date: ISO formatted start date string. Defaults to ``2024-01-01``.
        to_date: ISO formatted end date string. Defaults to ``2024-01-02``.
    """

    # Basic validation – ensure provided dates are parseable.
    try:
        datetime.date.fromisoformat(from_date)
        datetime.date.fromisoformat(to_date)
    except ValueError:
        # If parsing fails, fall back to defaults.
        from_date = "2024-01-01"
        to_date = "2024-01-02"

    query_info = QueryInfo(**{"from": from_date, "to": to_date})

    return GraphResponse(
        query_info=query_info,
        company_nodes=MOCK_COMPANIES,
        keyword_nodes=MOCK_KEYWORDS,
        edges=MOCK_EDGES,
    )
