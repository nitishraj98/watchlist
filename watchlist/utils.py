import aiohttp
import asyncio

# Replace with your own API key
API_KEY = '87cd0353f4msh42cd54be37719a8p190524jsn153f5fd0829d' 

# Function to fetch stock prices using the Yahoo Finance API
async def fetch_stock_prices(symbols):
    url = "https://yfapi.net/v6/finance/quote"
    
    async with aiohttp.ClientSession() as session:
        # Construct a list of tasks to fetch data for each symbol
        tasks = []
        for symbol in symbols:
            params = {'symbols': symbol}
            headers = {
                'x-api-key': API_KEY  # Add your API key here
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
                    'price_change_1M': 'N/A',  # You can fetch 1-month change if available from the API
                    'price_change_3M': 'N/A',  # Same here
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
