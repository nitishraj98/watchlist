from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Watchlist
from .serializers import RegisterSerializer, WatchlistSerializer
from .utils import fetch_stock_prices
import asyncio

# User Registration API
class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Watchlist Management
class WatchlistAdd(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        symbol = request.data.get('symbol')
        if not symbol:
            return Response({'error': 'Symbol is required'}, status=status.HTTP_400_BAD_REQUEST)

        Watchlist.objects.create(user=request.user, symbol=symbol)
        cache.delete(f'watchlist_{request.user.id}') 
        return Response({'message': 'Stock added to watchlist'}, status=status.HTTP_201_CREATED)

class WatchlistRetrieve(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f'watchlist_{request.user.id}'
        watchlist = cache.get(cache_key)

        if not watchlist:
            watchlist = Watchlist.objects.filter(user=request.user)
            serializer = WatchlistSerializer(watchlist, many=True)
            watchlist = serializer.data
            cache.set(cache_key, watchlist, timeout=300)

        return Response({'watchlist': watchlist})

class WatchlistRemove(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        symbol = request.data.get('symbol')
        if not symbol:
            return Response({'error': 'Symbol is required'}, status=status.HTTP_400_BAD_REQUEST)

        watchlist_item = Watchlist.objects.filter(user=request.user, symbol=symbol).first()
        if not watchlist_item:
            return Response({'error': 'Symbol not found in your watchlist'}, status=status.HTTP_404_NOT_FOUND)

        watchlist_item.delete()
        cache.delete(f'watchlist_{request.user.id}') 
        return Response({'message': 'Stock removed from watchlist'}, status=status.HTTP_204_NO_CONTENT)

class WatchlistPriceChanges(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        watchlist = Watchlist.objects.filter(user=request.user)
        symbols = [item.symbol for item in watchlist]

        price_data = asyncio.run(fetch_stock_prices(symbols))

        return Response({
            'user_id': request.user.id,
            'watchlist': [
                {
                    'symbol': symbols[i],
                    'current_price': price_data[i]['current_price'],
                    'price_change_1D': price_data[i]['price_change_1D'],
                    'price_change_1M': price_data[i]['price_change_1M'],
                    'price_change_3M': price_data[i]['price_change_3M'],
                }
                for i in range(len(symbols))
            ]
        })

