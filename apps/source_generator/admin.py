from django.contrib import admin
from .models import SourceSearch, Source


class SourceInline(admin.TabularInline):
    model = Source
    fields = ('position', 'title', 'link', 'snippet')
    readonly_fields = ('position', 'title', 'link', 'snippet')
    extra = 0


@admin.register(SourceSearch)
class SourceSearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'topic', 'limit', 'source_count', 'created_at')
    list_filter = ('user',)
    search_fields = ('topic', 'user__username')
    inlines = [SourceInline]

    def source_count(self, obj):
        return obj.sources.count()
    source_count.short_description = 'Sources'


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'title', 'link', 'search')
    list_filter = ('search__user',)
    search_fields = ('title', 'link', 'snippet')
