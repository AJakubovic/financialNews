from django.urls import include, path
from rest_framework import routers
from .views import (FeedsViewSet, FeedNewsViewSet, SymbolsViewSet, 
					feeds_api_get_by_symbol, get_news, get_news_by_multiple_symbols, get_new_news)


# genericki url:
router = routers.DefaultRouter()
router.register(r'feeds', FeedsViewSet)
router.register(r'feedNews', FeedNewsViewSet, basename='Financial news')
router.register(r'symbols', SymbolsViewSet)

# ostali oblici url:
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("feedsApi/<str:my_symbol>/", feeds_api_get_by_symbol.as_view(), name="feeds_by_symbol"),
    path("feedsApi/", feeds_api_get_by_symbol.as_view()),
    path("feedNewsApi/<str:my_symbol>/", get_news.as_view(), name="feedNews_by_symbol"),
    path("feedNewsApi/", get_news.as_view()),
    path("feedNewsMultipleSymbolsApi/<str:symbols>/", get_news_by_multiple_symbols.as_view(), name="feedNews_by_mul_symbols"),
    path("feedNewsMultipleSymbolsApi/", get_news_by_multiple_symbols.as_view()),
    path("feedNewNews/", get_new_news.as_view()),
]