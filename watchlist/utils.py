import aiohttp
import asyncio

async def fetch_stock_prices(symbols):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(f'https://mock-api.yahoo-finance.com/{symbol}') for symbol in symbols]
        responses = await asyncio.gather(*tasks)
        return [await response.json() for response in responses]
