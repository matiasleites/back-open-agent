from typing import Optional
from fastapi import APIRouter, Depends, Query
from repositories.articles_repository import ArticlesRepository
from api.schemas.responseSchemas import Article

router = APIRouter()

@router.get("/api/agent/article", response_model=Article)
async def create_article(
    about: str = Query(..., description="The topic about of the article"),
):
    articles_repository = ArticlesRepository()
    result = await articles_repository.create_article(about)
    return result