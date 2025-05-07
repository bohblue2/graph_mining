from fastapi import FastAPI
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



@app.get("/")
async def root():
    return {"message": "Graph Mining API"}


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
            },
            {
                "type": "company",
                "ISIN": "US0378331005",
                "name": "Apple",
                "priceFrom": 170.34,
                "priceTo": 172.80,
                "priceChange": 1.0144417048,
                "currency": "USD",
                "market": "NASDAQ",
                "source": "Yahoo Finance",
            },
            {
                "type": "company",
                "ISIN": "US0231351067",
                "name": "Amazon",
                "priceFrom": 150.10,
                "priceTo": 153.20,
                "priceChange": 1.0206528981,
                "currency": "USD",
                "market": "NASDAQ",
                "source": "Yahoo Finance",
            },
            {
                "type": "company",
                "ISIN": "US5949181045",
                "name": "Microsoft",
                "priceFrom": 400.50,
                "priceTo": 405.70,
                "priceChange": 1.0129837703,
                "currency": "USD",
                "market": "NASDAQ",
                "source": "Yahoo Finance",
            },
            {
                "type": "company",
                "ISIN": "US88160R1014",
                "name": "Tesla",
                "priceFrom": 250.00,
                "priceTo": 255.00,
                "priceChange": 1.02,
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
            },
            {
                "type": "keyword",
                "keyword": "iPhone",
                "priceChange": 1.0144417048,
            },
            {
                "type": "keyword",
                "keyword": "Mac",
                "priceChange": 1.0100000000,
            },
            {
                "type": "keyword",
                "keyword": "AWS",
                "priceChange": 1.0206528981,
            },
            {
                "type": "keyword",
                "keyword": "E-commerce",
                "priceChange": 1.0150000000,
            },
            {
                "type": "keyword",
                "keyword": "Azure",
                "priceChange": 1.0129837703,
            },
            {
                "type": "keyword",
                "keyword": "Windows",
                "priceChange": 1.0050000000,
            },
            {
                "type": "keyword",
                "keyword": "EV",
                "priceChange": 1.02,
            },
            {
                "type": "keyword",
                "keyword": "Autopilot",
                "priceChange": 1.03,
            }
        ],
        "edges":[
            {
                "source": "NVIDIA",
                "target": "AI 칩",
                "weight": 0.9,
            },
            {
                "source": "Apple",
                "target": "iPhone",
                "weight": 0.85,
            },
            {
                "source": "Apple",
                "target": "Mac",
                "weight": 0.75,
            },
            {
                "source": "Amazon",
                "target": "AWS",
                "weight": 0.92,
            },
            {
                "source": "Amazon",
                "target": "E-commerce",
                "weight": 0.88,
            },
            {
                "source": "Microsoft",
                "target": "Azure",
                "weight": 0.90,
            },
            {
                "source": "Microsoft",
                "target": "Windows",
                "weight": 0.70,
            },
            {
                "source": "Tesla",
                "target": "EV",
                "weight": 0.95,
            },
            {
                "source": "Tesla",
                "target": "Autopilot",
                "weight": 0.80,
            }
        ]
    }