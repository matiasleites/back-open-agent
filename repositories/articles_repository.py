from typing import Optional
from api.schemas.responseSchemas import Article
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from dotenv import load_dotenv
import os
import json

from tools.tools import search_tool, wiki_tool
load_dotenv()


class ArticlesRepository:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))
        self.parser = PydanticOutputParser(pydantic_object=Article)

    async def create_article(self, query: str, lang: Optional[str] = 'pt') -> Article:
        """
        Search for a query in the web and create and return a article.
        """

        if lang is None:
            lang = 'pt'
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """You are a helpful assistant that searches for valid articles in the web and wikipedia and use the information to create a brand new article.
                The article must be about the query and must be a new article that is not already in the web.
                The article must be written in a way that is easy to understand and is not too short and have to be mainstream and good to seo.
                
                IMPORTANT: You MUST write the article in the specified language ({lang}). 
                - If the language is 'pt', write the article in Brazilian Portuguese
                - If the language is 'es', write the article in Spanish
                - If the language is 'en', write the article in English
                - Always respect the language parameter and write the entire article in that language
                
                You must return the results in the following JSON format:
                {{
                    "title": "Article Title in the specified language",
                    "body": "The body of the new article that you created in the specified language",
                    "references": ["references to the sources that you used to create the article"]
                }}
                
                Make sure to return exactly this JSON format with the article found in the correct language."""),
                ("user", "Search for articles from the web and wikipedia based on the query: {query} and return a article in JSON format. CRITICAL: The language of the article MUST be {lang}. Write the entire article in {lang}."),
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
        raw_response = agent_executor.invoke({"query": query, "lang": lang})

        try:
            if "output" in raw_response and raw_response["output"]:
                output_text = raw_response["output"]
                if isinstance(output_text, list) and len(output_text) > 0:
                    output_text = output_text[0]["text"]
                
                # Try to extract JSON from the response
                import re
                
                # Look for JSON in the response
                json_match = re.search(r'\{.*\}', output_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    parsed_data = json.loads(json_str)
                    return Article(**parsed_data)
                else:
                    # If no JSON found, try to parse directly
                    structured_response = self.parser.parse(output_text)
                    return structured_response
            else:
                return Article(title="", body="", references=[])
        except Exception as e:
            print("Error parsing response", e, "Raw Response - ", raw_response)
            return Article(title="", body="", references=[])