from django.contrib import admin
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display   = ['title', 'author', 'category', 'status', 'created_at']
    list_filter    = ['status', 'category', 'created_at']
    search_fields  = ['title', 'body', 'author__username']
    raw_id_fields  = ['author']