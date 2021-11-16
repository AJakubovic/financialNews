from rest_framework import serializers
from .models import Feed, Symbol, FeedNews


class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = [
            "name",
            "active",
        ]
        extra_kwargs = {
            "active": {"required": False},
        }


class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = [
            "name",
            "url",
        ]

class FeedNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedNews
        fields = [
            "title",
            "description",
            "guid",
            "link",
            "pubDate",
            "s",
        ]