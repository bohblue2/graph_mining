from fastapi import FastAPI
from typing import List
from graph_mining.entity import Node, Company, Keyword, Edge

app = FastAPI()

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