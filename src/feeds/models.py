from django.db import models

# model FeedNews - koji predstavlja finansijsku vijest
class FeedNews(models.Model):
	title		= models.CharField(max_length=300)
	description	= models.TextField(max_length=1000)
	guid		= models.CharField(max_length=70)
	link		= models.URLField(max_length=500)
	pubDate		= models.DateTimeField()
	s           = models.CharField(max_length=10)

	# nazivi koji se koriste za singular i plural na admin modulu:
	class Meta:
		verbose_name = "feed news"
		verbose_name_plural = "feed news"

	# metoda dobavljanja linka
	def get_absolute_url(self):
		return f"{self.link}"

	def __str__(self):
		return self.title

# model Symbol - koji predstavlja simbol
class Symbol(models.Model):
	name 	= models.CharField(max_length=128)
	url 	= models.URLField(max_length=300)

	# nazivi koji se koriste za singular i plural na admin modulu:
	class Meta:
		verbose_name 		= "symbol"
		verbose_name_plural = "symbols"

	# def __str__(self):
	# 	return self.name

# model Feeds - koji predstavlja feed, odnosno informacije za koje sve kompanije se prikupljaju RSS feed-ovi
class Feed(models.Model):
	name 		= models.CharField(max_length=128)
	active 		= models.BooleanField(default=True)
	symbols 	= models.ManyToManyField(Symbol) # mapiranje sa objektima tipa Symbol - da bi jedan feed mogao biti vezan za vise simbola
												 # npr. GOLDFeed ima vezu sa simbolima GC=F i GOLD

	# nazivi koji se koriste za singular i plural na admin modulu:
	class Meta:
		verbose_name 		= "feed"
		verbose_name_plural = "feeds"

	# def __str__(self):
	# 	return self.name
