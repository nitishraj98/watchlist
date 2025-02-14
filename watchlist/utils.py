import aiohttp
import asyncio

API_KEY = '87cd0353f4msh42cd54be37719a8p190524jsn153f5fd0829d' 

async def fetch_stock_prices(symbols):
    url = "https://yfapi.net/v6/finance/quote"
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for symbol in symbols:
            params = {'symbols': symbol}
            headers = {
                'x-api-key': API_KEY  
            }
            task = session.get(url, headers=headers, params=params)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        # Parse the responses to extract the data
        price_data = []
        for response in responses:
            data = await response.json()
            if 'quoteResponse' in data and 'result' in data['quoteResponse']:
                result = data['quoteResponse']['result'][0]
                price_data.append({
                    'symbol': result['symbol'],
                    'current_price': result['regularMarketPrice'],
                    'price_change_1D': result['regularMarketChange'],
                    'price_change_1M': 'N/A',  
                    'price_change_3M': 'N/A', 
                })
            else:
                price_data.append({
                    'symbol': symbol,
                    'current_price': 'N/A',
                    'price_change_1D': 'N/A',
                    'price_change_1M': 'N/A',
                    'price_change_3M': 'N/A',
                })
        
        return price_data
