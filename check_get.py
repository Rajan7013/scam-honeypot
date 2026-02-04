import httpx
import asyncio

async def check():
    url = "http://localhost:8000/hackathon/chat"
    try:
        print(f"Checking {url}...")
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(check())
