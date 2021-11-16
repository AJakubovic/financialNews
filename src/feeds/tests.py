from django.test import TestCase
from .models import Feed, Symbol, FeedNews
from dateutil import parser
import feedparser

class FeedNewsTestCase(TestCase):

	# kreiranje objekata tipa Feed:
	def create_feeds(self):

		f_list = []
		f_list.append(Feed.objects.create(name="AAPLFeed", active=True))
		f_list.append(Feed.objects.create(name="INTCFeed", active=True))
		f_list.append(Feed.objects.create(name="GOLDFeed", active=True))
		f_list.append(Feed.objects.create(name="TWTRFeed", active=True))
		return f_list

	# kreiranje objekata tipa Symbol:
	def create_symbols(self):

		s_list = []
		s_list.append(Symbol.objects.create(name="AAPL", url="https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL&region=US&lang=en-US"))
		s_list.append(Symbol.objects.create(name="TWTR", url="https://feeds.finance.yahoo.com/rss/2.0/headline?s=TWTR&region=US&lang=en-US"))
		s_list.append(Symbol.objects.create(name="GC=F", url="https://feeds.finance.yahoo.com/rss/2.0/headline?s=GC=F&region=US&lang=en-US"))
		s_list.append(Symbol.objects.create(name="INTC", url="https://feeds.finance.yahoo.com/rss/2.0/headline?s=INTC&region=US&lang=en-US"))
		s_list.append(Symbol.objects.create(name="GOLD", url="https://feeds.finance.yahoo.com/rss/2.0/headline?s=GOLD&region=US&lang=en-US"))
		return s_list

	# kreiranje objekata tipa FeedNews:
	def create_feedNews(self):

		fn_list = []
		fn_list.append(FeedNews.objects.create(title="UPDATE 1-At least one person killed in protest near Barrick's Congo mine", 
			description="At least one person was killed during protests last week against evictions of people in illegal settlements near Barrick Gold Corp's Kibali gold mine in northeast Democratic Republic of Congo, the local governor's office said on Monday.  Two villages near the mine, where residents had previously been resettled from, have been occupied by local people, ""in violation of the rights of the company Kibali goldmines,"" the Haut Uele governor's office said in a statement.  ""Shots were fired and at least one death and several wounded have been confirmed,"" the governor's office said, referring to Friday's confrontation between settlers and police in the nearby town of Durba.", 
			guid="65c95bcc-0138-317b-93ab-af5165507708", 
			link="https://finance.yahoo.com/news/1-least-one-person-killed-222907873.html?.tsrc=rss", 
			pubDate="2021-10-26 00:29:07+02", 
			s="GOLD"))
		fn_list.append(FeedNews.objects.create(title="McAfee Nears Deal To Sell Itself For Over $10B: All You Need To Know", 
			description="McAfee Corp (NASDAQ: MCFE) is nearing a deal to sell itself to a group including private-equity firms Advent International Corp and Permira for over $10 billion, the Wall Street Journal reports. The deal could value McAfee at $25 a share, implying a 1.8% downside on McAfee's November 5 closing price of $25.46. The company's stock gained 20% on Friday. McAfee makes software that protects users against computer viruses, malware, and other online threats. McAfee, which returned to the public market", 
			guid="0fc5cd79-39e4-36f4-b1dd-404b6747d94b", 
			link="https://finance.yahoo.com/news/mcafee-nears-deal-sell-itself-111256969.html?.tsrc=rss", 
			pubDate="2021-11-08 12:12:56+01", 
			s="INTC"))
		return fn_list

	# spremanje jednog objekta tipa FeedNews:
	def post_single_feedNews(self, my_title, my_description, my_guid, my_link, my_pubDate, my_s):

		return FeedNews.objects.create(title=my_title, 
			description=my_description, 
			guid=my_guid, 
			link=my_link, 
			pubDate=my_pubDate, 
			s=my_s)

	# funkcija za vracanje url-a iz objekta Symbol prema proslijedjenom nazivu Feed-a:
	def get_url(self, name):

		s_list = self.create_symbols()
		s_obj = []
		for s in s_list:
			if s.name == name:
				s_obj = s
		return s_obj.url

	# provjera da li je uspjesno kreiranje objekata FeedNews iz funkcije create_feedNews: 
	def test_feedNews_creation(self):

		fn_list = self.create_feedNews()
		for fn in fn_list:
			self.assertTrue(isinstance(fn, FeedNews))
			self.assertEqual(fn.__str__(), fn.title)
			if fn.link == "https://finance.yahoo.com/news/mcafee-nears-deal-sell-itself-111256969.html?.tsrc=rss":
				self.assertEqual(fn.get_absolute_url(), fn.link)

	# provjera da li funkcija uspjesno vraca nove finansijske vijesti:
	def test_get_new_feed_news(self):

		rss_feeds = self.create_feeds()
		data_all = []
		new_feedNews = []

		lastNewsDate = "2021-10-21 00:29:07+02" # primjer starijeg datuma za kojeg bi funkcija trebala vratiti nove vijesti

		for feed in rss_feeds:
			if feed.active is False:
				continue
			s = feed.name[:4] # uzimamo substring prva cetiri slova iz naziva (npr. AAPL iz AAPLFeed) radi potreba testiranja
			data = feedparser.parse(self.get_url(name=s))
			length = data["entries"].__len__()
			for d in data["entries"][:length]: 
				d["published"] = parser.parse(d["published"]).strftime('%Y-%m-%d %H:%M:%S.%f%z') 
				# iz formata se izbacuje day in the week, kako bi sortiranje po datumu radilo kako se ocekuje
				if parser.parse(d["published"]) > parser.parse(lastNewsDate):
					data_all.append(d)
		
		sorted_data = list(sorted(data_all, key=lambda i: i["published"])) # sortiranje po datumu ascending

		for news in sorted_data:
			new_element = {}
			new_element["title"] = news["title"]
			new_element["description"] = news["description"]
			new_element["guid"] = news["id"]
			new_element["link"] = news["link"]
			new_element["pubDate"] = parser.parse(news["published"])
			new_element["s"] = news["title_detail"]["base"].split("s=")[1].split("&region")[0]
			new_feedNews.append(new_element)
			self.post_single_feedNews(my_title=new_element["title"], # provjera kreiranja novog objekta
				my_description=new_element["description"], 
				my_guid=new_element["guid"], 
				my_link=new_element["link"], 
				my_pubDate=new_element["pubDate"], 
				my_s=new_element["s"])
		
		self.assertTrue(new_feedNews.__len__() > 0) # za postavljeni datum od 21.10.2021. bi moralo biti vraceno novih vijesti

		return new_feedNews
