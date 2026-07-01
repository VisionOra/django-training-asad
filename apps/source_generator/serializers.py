from rest_framework import serializers
from .models import SourceSearch, Source


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('id', 'title', 'link', 'snippet', 'position')


class SourceSearchListSerializer(serializers.ModelSerializer):
    """Lightweight — used for list endpoint (no sources payload)."""
    source_count = serializers.SerializerMethodField()

    class Meta:
        model = SourceSearch
        fields = ('id', 'topic', 'limit', 'source_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_source_count(self, obj) -> int:
        return obj.sources.count()


class SourceSearchSerializer(serializers.ModelSerializer):
    """Full detail — includes all fetched sources."""
    sources = SourceSerializer(many=True, read_only=True)
    source_count = serializers.SerializerMethodField()

    class Meta:
        model = SourceSearch
        fields = ('id', 'topic', 'limit', 'source_count', 'sources', 'created_at', 'updated_at')
        read_only_fields = ('id', 'source_count', 'sources', 'created_at', 'updated_at')

    def get_source_count(self, obj) -> int:
        return obj.sources.count()
