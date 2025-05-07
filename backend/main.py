from fastapi import FastAPI
from typing import List
from tg_api.entity import Node, Company, Keyword, Edge
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# Mock data
mock_companies: List[Company] = [
    {"id": "AAPL", "stock_1d": 2.5, "stock_1w": 5.3, "stock_1m": 12.7},
    {"id": "GOOGL", "stock_1d": -1.2, "stock_1w": 3.8, "stock_1m": 8.4},
    {"id": "MSFT", "stock_1d": 1.8, "stock_1w": 4.2, "stock_1m": 10.1},
    {"id": "AMZN", "stock_1d": 0.5, "stock_1w": 2.1, "stock_1m": 7.5}
]

mock_keywords: List[Keyword] = [
    {"id": "tech", "name": "Technology"},
    {"id": "ai", "name": "Artificial Intelligence"},
    {"id": "cloud", "name": "Cloud Computing"},
    {"id": "ecommerce", "name": "E-commerce"}
]

mock_edges: List[Edge] = [
    {"company": "AAPL", "keyword": "tech", "weight": 0.9},
    {"company": "AAPL", "keyword": "ai", "weight": 0.6},
    {"company": "GOOGL", "keyword": "tech", "weight": 0.95},
    {"company": "GOOGL", "keyword": "ai", "weight": 0.9},
    {"company": "GOOGL", "keyword": "cloud", "weight": 0.8},
    {"company": "MSFT", "keyword": "tech", "weight": 0.92},
    {"company": "MSFT", "keyword": "ai", "weight": 0.85},
    {"company": "MSFT", "keyword": "cloud", "weight": 0.88},
    {"company": "AMZN", "keyword": "tech", "weight": 0.85},
    {"company": "AMZN", "keyword": "cloud", "weight": 0.9},
    {"company": "AMZN", "keyword": "ecommerce", "weight": 0.98}
]

@app.get("/")
async def root():
    return {"message": "Graph Mining API"}

@app.get("/node", response_model=Node)
async def get_node():
    return {
        "company": mock_companies,
        "keyword": mock_keywords,
        "edge": mock_edges
    }

@app.get("/companies", response_model=List[Company])
async def get_companies():
    return mock_companies

@app.get("/keywords", response_model=List[Keyword])
async def get_keywords():
    return mock_keywords

@app.get("/edges", response_model=List[Edge])
async def get_edges():
    return mock_edges 

@app.get("/test")
async def test():
    return {
        "query_info":{
            "from": "2024-01-01",
            "to": "2024-01-02"
        },
        "company_nodes":[
            {
                "type": "company",
                "ISIN": "US67066G1040",
                "name": "NVIDIA",
                "priceFrom": 113.54,
                "priceTo": 115.54,
                "priceChange": 1.0176149375,
                "currency": "USD",
                "market": "NASDAQ",
                "source": "Yahoo Finance",
            }
        ],
        "keyword_nodes":[
            {
                "type": "keyword",
                "keyword": "AI 칩",
                "priceChange": 1.0176149375,
            }
        ],
        "edges":[
            {
                "source": "NVIDIA",
                "target": "AI 칩",
                "weight": 0.5,
            }
        ]
    }