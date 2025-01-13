
from fastapi import FastAPI, HTTPException
from httpx import AsyncClient
import random
import abc


class GenerationService(abc.ABC):
    @abc.abstractmethod
    async def generate_random_article_idea(self) -> str:
        pass

    @abc.abstractmethod
    async def generate_technical_guide(self) -> str:
        pass

    @abc.abstractmethod
    async def generate_fiction(self) -> str:
        pass


class ArticleGenerationService(GenerationService):
    async def generate_random_article_idea(self) -> str:
        ideas = ["The future of AI", "The rise of async programming", "Best practices in API design"]
        return random.choice(ideas)

    async def generate_technical_guide(self) -> str:
        guides = ["How to use FastAPI with httpx", "Async programming in Python", "Building scalable APIs"]
        return random.choice(guides)

    async def generate_fiction(self) -> str:
        stories = ["A world where AI rules", "A coder's journey to the center of the web", "The async saga"]
        return random.choice(stories)


app = FastAPI()
service = ArticleGenerationService()

@app.get("/generate-article")
async def generate_article(type: str):
    if type not in ["random", "technical", "fiction"]:
        raise HTTPException(status_code=400, detail="Invalid article type")

    if type == "random":
        return {"idea": await service.generate_random_article_idea()}
    elif type == "technical":
        return {"idea": await service.generate_technical_guide()}
    elif type == "fiction":
        return {"idea": await service.generate_fiction()}
