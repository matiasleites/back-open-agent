from typing import Optional
from fastapi import APIRouter, Depends, Query
from repositories.articles_repository import ArticlesRepository
from api.schemas.responseSchemas import ArticlesResearchResponse

router = APIRouter()

@router.get("/api/agent/articles", response_model=ArticlesResearchResponse)
async def search_articles(
    query: str = Query(..., description="The query to search for"),
    limit: Optional[int] = Query(5, description="The number of results to return")
):
    articles_repository = ArticlesRepository()
    result = await articles_repository.search_articles(query, limit)
    return result