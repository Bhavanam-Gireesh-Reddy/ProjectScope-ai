from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str

class Repo(BaseModel):
    id: str
    name: str
    description: Optional[str]
    url: str
    stars: int
    technologies: List[str]

class Paper(BaseModel):
    id: str
    title: str
    authors: List[str]
    year: int
    url: str
    abstract: str
    citations: int
    influential_citations: Optional[int] = 0

class Dataset(BaseModel):
    id: str
    title: str
    url: str
    description: Optional[str] = None
    downloads: Optional[int] = 0

class SearchResponse(BaseModel):
    repositories: List[Repo]
    papers: List[Paper]
    datasets: List[Dataset] = []
    insights: str
    roadmap: List[str]
    confidence_score: float
