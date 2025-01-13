
import asyncio
import httpx
import argparse

BASE_URL = "http://127.0.0.1:8000"

async def article_idea(client: httpx.AsyncClient, article_type: str):
    response = await client.get(f"{BASE_URL}/generate-article", params={"type": article_type})
    response.raise_for_status()
    data = response.json()
    print(f"Generated Idea: {data['idea']}")

async def main():
    parser = argparse.ArgumentParser(description="Article Idea Generator")
    parser.add_argument("type", choices=["random", "technical", "fiction"], help="Type of article to generate")
    args = parser.parse_args()

    async with httpx.AsyncClient() as client:
        await article_idea(client, args.type)

if __name__ == "__main__":
    asyncio.run(main())
