# 테마주 Graph 분석도구

## Crawling

### 1. 뉴스 기반 회사 - 키워드 크롤링

뉴스 기반으로 회사와 키워드간의 관계를 파악하여 키워드 그래프를 구축합니다. 이 과정에서 gpt-4o-mini 모델을 사용할 예정입니다.

Data Schema는 다음과 같습니다.

```json
{
  "article_url": "https://example.com",
  "date": "YYYY-MM-DD",
  "links": [
    {
      "companyName": "회사명",
      "ISIN": "국제증권식별번호",
      "keyword": "핵심 키워드",
      "weight": 1.0, // -1.0 ~ 1.0 사이의 값 (-1.0 강한 부정, 0 중립, 1.0 강한 긍정)
      "context": "어떠한 키워드가 어떠한 회사에 대해 어떠한 영향을 주었는지 설명"
    }
  ]
}
```

gpt-4o-mini 모델에게 전달할 프롬프트는 다음과 같습니다.


```plaintext
너는 뉴스 기사를 분석해서 기업과 키워드 간의 의미 있는 관계를 추출하는 역할을 한다.

다음 조건에 따라 각 기사에서 "기업", "키워드", "긍·부정 정도 (weight)", 그리고 "맥락 설명 (context)"을 구성하여 JSON 형태로 출력해라.

📌 JSON 스키마는 아래와 같다:

{
  "article_url": "뉴스 기사 URL",
  "date": "YYYY-MM-DD",
  "links": [
    {
      "companyName": "회사명",
      "ISIN": "국제증권식별번호 (가능하면 실제 코드, 없으면 PLACEHOLDER)",
      "keyword": "핵심 키워드",
      "weight": -1.0 ~ 1.0 사이 값 (해당 키워드가 회사에 부정적이면 음수, 긍정적이면 양수, 중립이면 0)",
      "context": "키워드가 해당 회사에 어떤 영향을 주는지 설명"
    },
    ...
  ]
}

예시:
뉴스 기사 본문:  
"젠슨 황 엔비디아 CEO는 미국 정부의 수출 제한이 오히려 화웨이 같은 경쟁사에 유리할 수 있다며, 미국 정책이 자국 기업에 불리하다고 지적했다. 그는 중국 시장에서 AI칩 수요가 여전히 강하다고 강조했다."

기사 URL: https://n.news.naver.com/mnews/article/032/0003368052  
기사 날짜: 2025-05-06

🎯 모델의 목표:
- 기사에서 등장한 기업 이름과 관련 키워드를 추출할 것
- 그 키워드가 해당 기업에 주는 긍·부정적 영향(정성적)을 분석해 정량화된 weight(-1 ~ 1)로 표현할 것
- 키워드-기업 관계에 대한 설명을 context로 작성할 것
- 가능하면 실제 ISIN 코드 포함 (없으면 PLACEHOLDER)

🛑 주의사항:
- 키워드는 테마주 키워드로 제한
- 중립적인 언급은 weight를 0 또는 ±0.1 수준으로
- 추론은 간결하고 명확하게
- 필요 없는 정보는 포함하지 말 것
- 최종 출력은 JSON만 포함할 것

[뉴스 기사 본문 삽입]
```

```json
// example
[{
  "article_url": "https://n.news.naver.com/mnews/article/032/0003368052",
  "date": "2025-05-06",
  "links": [
    {
      "companyName": "NVIDIA",
      "ISIN": "US67066G1040",
      "keyword": "미국 행정부",
      "weight": -0.7,
      "context": "미국 행정부의 수출 제한 정책이 NVIDIA의 중국 시장 접근을 가로막고 있어 부정적인 영향을 주고 있음"
    },
    {
      "companyName": "NVIDIA",
      "ISIN": "US67066G1040",
      "keyword": "AI칩",
      "weight": 0.5,
      "context": "NVIDIA는 H100 및 H20과 같은 AI칩을 통해 글로벌 AI 기술 리더십을 보유하고 있으며, 이는 긍정적인 평가를 받음"
    },
    {
      "companyName": "NVIDIA",
      "ISIN": "US67066G1040",
      "keyword": "수출 통제",
      "weight": -0.6,
      "context": "미국 정부의 수출 통제로 인해 NVIDIA의 매출 기회가 줄어들 수 있어 부정적 영향이 있음"
    },
    {
      "companyName": "Huawei",
      "ISIN": "CNE100000QF3",
      "keyword": "고성능 반도체",
      "weight": 0.6,
      "context": "NVIDIA의 공백을 틈타 화웨이가 고성능 반도체 시장에서 입지를 강화하고 있음"
    },
    {
      "companyName": "Huawei",
      "ISIN": "CNE100000QF3",
      "keyword": "AI칩 자체 개발",
      "weight": 0.7,
      "context": "화웨이가 H100 수준의 AI칩을 자체 개발 중이라는 보도가 나와 기술 경쟁력 강화로 이어질 가능성이 있음"
    }
  ]
}, ... ]
```

### 2. 회사별 주식 지표 크롤링

```json
[{
  "company": "NVIDIA",
  "ISIN": "US67066G1040",
  "date": "2025-05-06",
  "open": 110.00,
  "close": 113.54,
  "high": 115.00,
  "low": 109.20,
  "volume": 25600000,
  "currency": "USD",
  "market": "NASDAQ",
  "source": "Yahoo Finance"
}, ... ]
```

## API 설계

```plaintext

GET /graph?from=2024-01-01&to=2024-01-02

1. 쿼리하는 기간을 완전히 포함하는 가장 짧은 기간의 주식 변동성을 모든 종목에 대해서 쿼리
2. 키워드 크롤링을 통해서 구축해둔 그래프에 회사별 주식 변동성 데이터 삽입
3. weight 값을 기반으로 키워드 그래프에 주식 변동성 데이터 추론 및 삽입
4. 추론된 데이터를 기반으로 키워드 리스트 정렬

그래프 데이터와 키워드 리스트를 반환

{
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
```
