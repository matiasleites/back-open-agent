from typing import Optional
from fastapi import APIRouter, Depends, Query
from repositories.articles_repository import ArticlesRepository
from api.schemas.responseSchemas import Article

router = APIRouter()

@router.get("/api/agent/article", response_model=Article)
async def create_article(
    about: str = Query(..., description="The topic about of the article"),
    lang: Optional[str] = Query('pt', description="The language of the article (default: pt-BR)"),
):
    articles_repository = ArticlesRepository()
    # Ensure lang is always set to pt-BR if not specified
    if lang is None:
        lang = 'pt'
    result = await articles_repository.create_article(about, lang)
    return result