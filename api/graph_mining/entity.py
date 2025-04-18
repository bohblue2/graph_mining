from typing import List, TypedDict, Optional

class Company(TypedDict):
    id: str
    stock_1d: float
    stock_1w: float
    stock_1m: float

class Keyword(TypedDict):
    id: str
    name: str

class Edge(TypedDict):
    company: str
    keyword: str
    weight: float

class Node(TypedDict):
    company: List[Company]
    keyword: List[Keyword]
    edge: List[Edge] 