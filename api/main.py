from fastapi import FastAPI
from typing import List
from graph_mining.entity import Node, Company, Keyword, Edge
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
    "nodes": [
        { "id": "반도체",          "type": "theme" },
        { "id": "2차전지",        "type": "theme" },
        { "id": "클라우드/AI",    "type": "theme" },
        { "id": "메타버스",        "type": "theme" },
        { "id": "헬스케어/바이오", "type": "theme" },

        { "id": "005930", "type": "stock", "code": "005930", "name": "삼성전자" },
        { "id": "000660", "type": "stock", "code": "000660", "name": "SK하이닉스" },
        { "id": "000990", "type": "stock", "code": "000990", "name": "DB하이텍" },

        { "id": "051910", "type": "stock", "code": "051910", "name": "LG화학" },
        { "id": "006400", "type": "stock", "code": "006400", "name": "삼성SDI" },
        { "id": "096770", "type": "stock", "code": "096770", "name": "SK이노베이션" },

        { "id": "035420", "type": "stock", "code": "035420", "name": "NAVER" },
        { "id": "035720", "type": "stock", "code": "035720", "name": "카카오" },
        { "id": "012510", "type": "stock", "code": "012510", "name": "더존비즈온" },

        { "id": "036570", "type": "stock", "code": "036570", "name": "엔씨소프트" },
        { "id": "112040", "type": "stock", "code": "112040", "name": "위메이드" },
        { "id": "078340", "type": "stock", "code": "078340", "name": "컴투스" },

        { "id": "068270", "type": "stock", "code": "068270", "name": "셀트리온" },
        { "id": "207940", "type": "stock", "code": "207940", "name": "삼성바이오로직스" },
        { "id": "000100", "type": "stock", "code": "000100", "name": "유한양행" }
    ],
    "links": [
        { "source": "반도체",       "target": "005930", "value": 0.88 },
        { "source": "반도체",       "target": "000660", "value": 0.84 },
        { "source": "반도체",       "target": "000990", "value": 0.75 },

        { "source": "2차전지",     "target": "051910", "value": 0.92 },
        { "source": "2차전지",     "target": "006400", "value": 0.89 },
        { "source": "2차전지",     "target": "096770", "value": 0.80 },

        { "source": "클라우드/AI", "target": "035420", "value": 0.78 },
        { "source": "클라우드/AI", "target": "035720", "value": 0.82 },
        { "source": "클라우드/AI", "target": "012510", "value": 0.65 },

        { "source": "메타버스",     "target": "036570", "value": 0.70 },
        { "source": "메타버스",     "target": "112040", "value": 0.68 },
        { "source": "메타버스",     "target": "078340", "value": 0.60 },

        { "source": "헬스케어/바이오","target": "068270","value": 0.85 },
        { "source": "헬스케어/바이오","target": "207940","value": 0.90 },
        { "source": "헬스케어/바이오","target": "000100","value": 0.72 },

        { "source": "005930","target":"000660","value":0.81,"type":"corr" },
        { "source": "051910","target":"006400","value":0.88,"type":"corr" },
        { "source": "068270","target":"207940","value":0.79,"type":"corr" }
    ]
    }