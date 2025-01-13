import asyncio
import random
import time
import argparse
import httpx

BASE_URL = "https://pokeapi.co/api/v2/pokemon/{pokemon_id}"


def get_urls(n: int) -> list[str]:
    return [BASE_URL.format(pokemon_id=random.randint(1, 500)) for _ in range(n)]


async def fetch_pokemon_httpx(url: str) -> str:
    async with httpx.AsyncClient() as client:
        print(f"Requesting {url} (httpx)")
        response = await client.get(url)
        response.raise_for_status()
        return response.json()["name"]


async def fetch_pokemon_aiohttp(url: str) -> str:
    from aiohttp import ClientSession

    async with ClientSession() as session:
        print(f"Requesting {url} (aiohttp)")
        async with session.get(url) as response:
            response.raise_for_status()
            return (await response.json())["name"]


def fetch_pokemon_requests(url: str) -> str:
    print(f"Requesting {url} (requests)")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["name"]


async def async_pokemons(fetcher, n: int = 50):
    urls = get_urls(n)
    tasks = [fetcher(url) for url in urls]
    return await asyncio.gather(*tasks)


def sync_pokemons(n: int = 50):
    urls = get_urls(n)
    return [fetch_pokemon_requests(url) for url in urls]


def main():
    parser = argparse.ArgumentParser(description="Fetch Pokémon data using async or sync HTTP requests.")
    parser.add_argument(
        "mode", choices=["httpx", "aiohttp", "requests"], help="Choose the library to fetch Pokémon data"
    )
    parser.add_argument("--count", type=int, default=50, help="Number of Pokémon to fetch")
    args = parser.parse_args()

    n = args.count
    start = time.perf_counter()

    if args.mode == "requests":
        data = sync_pokemons(n)
    else:
        fetcher = fetch_pokemon_httpx if args.mode == "httpx" else fetch_pokemon_aiohttp
        data = asyncio.run(async_pokemons(fetcher, n))

    end = time.perf_counter()

    print(f"\nFetched Pokémon names ({args.mode}): {data}")
    print(f"The number of Pokémon fetched: {len(data)}")
    print(f"Execution time: {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
