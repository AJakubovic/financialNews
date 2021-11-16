from django.contrib import admin

from feeds.models import Feed, Symbol, FeedNews

# registracija objekata u admin modulu, kako bi se i na taj nacin mogli kreirati u db:
admin.site.register(Feed)
admin.site.register(Symbol)
admin.site.register(FeedNews)
