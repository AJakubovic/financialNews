from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Feed, Symbol, FeedNews
from .tasks import get_new_feed_news
from .serializers import FeedSerializer, SymbolSerializer, FeedNewsSerializer
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django_celery_beat.models import PeriodicTask
from dateutil import parser


# glavni REST api za objekte tipa Feed, koji implementira metode GET, POST, PUT, DELETE:
# http://localhost:8000/feeds/
class FeedsViewSet(ModelViewSet):
	queryset = Feed.objects.all().order_by('name') # sortiranje po name ascending
	serializer_class = FeedSerializer

# glavni REST api za objekte tipa FeedNews, koji implementira samo metodu GET 
# (read only model jer ne zelimo da korisnik moze dodati, izmijeniti ili obrisati vijest):
# http://localhost:8000/feedNews/
class FeedNewsViewSet(ReadOnlyModelViewSet): 
	queryset = FeedNews.objects.all().order_by('-pubDate') # sortiranje po pubDate descending
	serializer_class = FeedNewsSerializer

	#drugi nacin za ogranicenje mogucnosti bi bio ModelViewSet uz dodatno postavljanje dozvoljenih metoda:
	#http_method_names = ['get', 'head']

# glavni REST api za objekte tipa Symbol, koji implementira metode GET, POST, PUT, DELETE:
# http://localhost:8000/symbols/
class SymbolsViewSet(ModelViewSet):
	queryset = Symbol.objects.all().order_by('name') # sortiranje po name ascending
	serializer_class = SymbolSerializer

#ostali view-i:

# api za dobavljanje Feed objekata po simbolu, 
# npr. http://localhost:8000/feedsApi/AAPL/, koji implementira samo GET metodu:
class feeds_api_get_by_symbol(APIView):

	permission_classes = (IsAuthenticatedOrReadOnly,)

	def get(self, request, **kwargs):
		my_symbol = kwargs.get('my_symbol', None)

		rss_feeds = []

		if my_symbol is not None:
				try:
					rss_feed = Feed.objects.get(symbols__name=my_symbol) # dobavljanje po proslijedjenom simbolu
					rss_feeds.append(rss_feed)
				except Feed.DoesNotExist:
					pass
		else:
			rss_feeds = Feed.objects.all() # u slucaju da simbol nije naveden iza / u url, vracaju se svi Feed objekti

		feeds = []
		for feed in rss_feeds:
			tmp_dict = model_to_dict(feed)
			tmp_dict["symbols"] = [x.name for x in feed.symbols.all()]
			feeds.append(tmp_dict)

		return Response(feeds, 200)


# api za dobavljanje FeedNews objekata po simbolu, 
# npr. http://localhost:8000/feedNewsApi/INTC/, koji implementira samo GET metodu:
class get_news(APIView, PageNumberPagination):

	permission_classes = (IsAuthenticatedOrReadOnly,)

	def get(self, request, **kwargs):

		my_symbol = kwargs.get('my_symbol', None)
		
		if my_symbol is not None:
			
				try:
					feed_news = FeedNews.objects.filter(s=my_symbol).order_by('-pubDate').values() 
					# dobavljanje po proslijedjenom simbolu i sortiranje po pubDate descending
				except FeedNews.DoesNotExist:
					pass
		else:
			feed_news = FeedNews.objects.all().order_by('-pubDate').values()
			# u slucaju da simbol nije naveden iza / u url, vracaju se svi FeedNews objekti, sortirani po pubDate descending
		
		results = self.paginate_queryset(feed_news, request, view=self) # paginacija rezultata
		return self.get_paginated_response(results)


# api za dobavljanje FeedNews objekata po više simbola, 
# npr. http://localhost:8000/feedNewsMultipleSymbolsApi/?symbols=AAPL,TWTR,INTC/ - implementira samo GET metodu:
class get_news_by_multiple_symbols(APIView, PageNumberPagination):

	permission_classes = (IsAuthenticatedOrReadOnly,)

	def get(self, request):

		symbols = request.GET.get("symbols", None)

		if symbols is not None:
			symbols = symbols.split(",") # simboli se odvajaju zarezima
			try:
				feed_news = FeedNews.objects.filter(s__in=symbols).order_by('-pubDate').values()
				# dobavljanje po proslijedjenim simbolima i sortiranje po pubDate descending
			except FeedNews.DoesNotExist:
				pass
		else:
			feed_news = FeedNews.objects.all().order_by('-pubDate').values()
			# u slucaju da simbol nije naveden iza / u url, vracaju se svi FeedNews objekti, sortirani po pubDate descending
		
		results = self.paginate_queryset(feed_news, request, view=self)  # paginacija rezultata
		return self.get_paginated_response(results)
		
# api za dobavljanje novih FeedNews objekata, koji jos nisu spremljeni u bazu 
# (to je lista vijesti koja bi se spremila pri narednom pustanju taska - scraping service-a) 
# npr. http://localhost:8000/feedNewNews/ - implementira samo GET metodu:
class get_new_news(APIView, PageNumberPagination):

	permission_classes = (IsAuthenticatedOrReadOnly,)

	def get(self, request):

		results = self.paginate_queryset(get_new_feed_news(), request, view=self)  # poziv metode sa tasks.py i 
																				   # paginacija rezultata
		return self.get_paginated_response(results)