from api.schemas.responseSchemas import ArticlesResearchResponse
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from dotenv import load_dotenv
import os

from tools.tools import search_tool, wiki_tool
load_dotenv()


class ArticlesRepository:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))
        self.parser = PydanticOutputParser(pydantic_object=ArticlesResearchResponse)

    async def search_articles(self, query: str, limit: int = 5) -> ArticlesResearchResponse:
        """
        Search for articles from the web and wikipedia and return a list of articles.
        """
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """You are a helpful assistant that searches for articles from the web and wikipedia based on the query.
                You must return the results in the following JSON format:
                {{
                    "articles": [
                        {{
                            "title": "Article Title",
                            "description": "Brief description of the article",
                            "image_url": "URL of the article image or a placeholder",
                            "link": "URL of the article",
                            "score": 0.95
                        }}
                    ]
                }}
                
                Make sure to return exactly this JSON format with the articles found."""),
                ("user", "Search for articles from the web and wikipedia based on the query: {query} and return a list of {limit} articles in JSON format."),
                ("assistant", "{agent_scratchpad}"),
            ]
        )
        
        tools = [search_tool, wiki_tool]

        agent = create_tool_calling_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt,
        )

        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        raw_response = agent_executor.invoke({"query": query, "limit": limit})

        try:
            if "output" in raw_response and raw_response["output"]:
                output_text = raw_response["output"]
                if isinstance(output_text, list) and len(output_text) > 0:
                    output_text = output_text[0]["text"]
                structured_response = self.parser.parse(output_text)
                return structured_response
            else:
                return ArticlesResearchResponse(articles=[])
        except Exception as e:
            print("Error parsing response", e, "Raw Response - ", raw_response)
            return ArticlesResearchResponse(articles=[])