from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

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
