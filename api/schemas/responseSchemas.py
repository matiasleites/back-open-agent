from pydantic import BaseModel

class Article(BaseModel):
    """
    Schema for an article.
    """
    title: str
    description: str
    image_url: str
    link: str
    score: float

class ArticlesResearchResponse(BaseModel):
    """
    Response schema for the articles research.
    """
    articles: list[Article]