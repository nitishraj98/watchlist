from django.urls import path
from .views import RegisterUser, WatchlistAdd, WatchlistRetrieve, WatchlistRemove, WatchlistPriceChanges
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('watchlist/add/', WatchlistAdd.as_view(), name='watchlist_add'),
    path('watchlist/', WatchlistRetrieve.as_view(), name='watchlist_retrieve'),
    path('watchlist/remove/', WatchlistRemove.as_view(), name='watchlist_remove'),
    path('watchlist/price-changes/', WatchlistPriceChanges.as_view(), name='watchlist_price_changes'),
]
