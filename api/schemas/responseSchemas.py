from pydantic import BaseModel

class Article(BaseModel):
    """
    Schema for an article.
    """
    title: str
    body: str
    sources: list[str]
