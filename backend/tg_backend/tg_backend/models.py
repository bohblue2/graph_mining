from pydantic import BaseModel, Field
from typing import List, Literal

class QueryInfo(BaseModel):
    """Information about the query time range."""

    from_date: str = Field(..., alias="from")
    to_date: str = Field(..., alias="to")

    class Config:
        validate_by_name = True


class CompanyNode(BaseModel):
    type: Literal["company"] = "company"
    ISIN: str
    name: str
    priceFrom: float
    priceTo: float
    priceChange: float
    currency: str
    market: str
    source: str


class KeywordNode(BaseModel):
    type: Literal["keyword"] = "keyword"
    keyword: str
    priceChange: float


class Edge(BaseModel):
    source: str
    target: str
    weight: float


class GraphResponse(BaseModel):
    query_info: QueryInfo
    company_nodes: List[CompanyNode]
    keyword_nodes: List[KeywordNode]
    edges: List[Edge]

    class Config:
        validate_by_name = True 