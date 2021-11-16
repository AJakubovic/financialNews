from celery import shared_task
from .models import Feed, Symbol, FeedNews
from django_celery_beat.models import PeriodicTask
from django.db import transaction
from datetime import datetime 
from dateutil import parser
import pytz
import feedparser
import django

django.setup()

# task za prikupljanje i spremanje novih finansijskih vijesti u bazu:
@shared_task
def saveNewFeedNews():

	news = get_new_feed_news() # poziv funkcije za prikupljanje novih finansijskih vijesti
	transaction.set_autocommit(False) # opcija koja omogucava postavku rollback i commit 
									  # (kada je True onda je defaultno sve commit)
	try:
		objs = [FeedNews(title=i["title"], description=i["description"],
						guid=i["guid"], link=i["link"], pubDate=i["pubDate"], s=i["s"]) for i in news]
		FeedNews.objects.bulk_create(objs) # bulk spremanje liste objekata FeedNews
		# pojedinacno spremanje bi bilo:
		# for i in news:
		# 	FeedNews.objects.create(title=i["title"], description=i["description"],
		# 	guid=i["guid"], link=i["link"], pubDate=i["pubDate"], s=i["s"])
	except:
		transaction.rollback() # ukoliko se desi neki izuzetak, ne sprema se nista u bazu
		raise
	else:
		transaction.commit() # u ovom trenutku transakcija se komita, ako se nije desio exception
	finally:
		transaction.set_autocommit(True) # vracanje defaultne postavke na True


# funkcija za prikupljanje novih finansijskih vijesti:
def get_new_feed_news():

	rss_feeds = Feed.objects.all()
	data_all = []
	new_feedNews = []

	# implementacija koja uzima datum zadnjeg pokretanja taska:
	#taskLastRunAt = PeriodicTask.objects.get(task='feeds.tasks.saveNewFeedNews').last_run_at
	
	# implementacija koja uzima datum zadnje pohranjene vijesti 
	# (ili postavlja 'datum od' na: 15.11.2021. u 9h - ukoliko je u pitanju prvo pokretanje taska i tabela feedNews je prazna)
	count = FeedNews.objects.all().count()
	if count > 0:
		lastNewsDate = FeedNews.objects.all()[count-1].pubDate
	else:
		lastNewsDate = datetime(2021, 11, 15, 9, 0, 0, 0, pytz.UTC) # timezone aware datumski objekat


	for feed in rss_feeds:
		if feed.active is False: # ako feed nije aktivan, znaci da ne zelimo prikupljati vijesti o toj kompaniji, nastavlja se dalje
			continue
		symbols = feed.symbols.all()
		
		for s in symbols:
			data = feedparser.parse(s.url)
			length = data["entries"].__len__() # broj unosa koji su pronadjeni nakon feedparse za rss feed url koji pripada simbolu s
			for d in data["entries"][:length]: 
				# konverzija formata datuma - izbacivanje day in the week, kako bi sortiranje u nastavku bilo ispravno
				d["published"] = parser.parse(d["published"]).strftime('%Y-%m-%d %H:%M:%S.%f%z')
				#if (taskLastRunAt is None) or (parser.parse(d["published"]) > taskLastRunAt):
				# (prvo punjenje tabele feedNews) ili (uzimanje samo novijih vijesti ukoliko je u pitanju naredno punjenje):
				if (lastNewsDate is None) or (parser.parse(d["published"]) > lastNewsDate):
					data_all.append(d)
				# to znaci da se vec spremljene vijesti nece ponovo spremati u tabelu, jer u nastavku radimo sa data_all listom vijesti
	
	sorted_data = list(sorted(data_all, key=lambda i: i["published"])) 
	# sortiranje po published ascending, kako bi uvijek na dnu tabele feedNews bile najnovije vijesti

	for news in sorted_data:
		# izdvajanje informacija potrebnih za tabelu feedNews u novi element, koji postaje clan liste new_feedNews koju funkcija vraca
		new_element = {}
		new_element["title"] = news["title"]
		new_element["description"] = news["description"]
		new_element["guid"] = news["id"]
		new_element["link"] = news["link"]
		new_element["pubDate"] = parser.parse(news["published"])
		new_element["s"] = news["title_detail"]["base"].split("s=")[1].split("&region")[0]
		new_feedNews.append(new_element)
	
	return new_feedNews
