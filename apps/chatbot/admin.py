from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    fields = ('role', 'content', 'created_at')
    readonly_fields = ('created_at',)
    extra = 0


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at', 'updated_at')
    list_filter = ('user',)
    search_fields = ('title', 'user__username')
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'role', 'content_preview', 'created_at')
    list_filter = ('role', 'session__user')
    search_fields = ('content',)

    def content_preview(self, obj):
        return obj.content[:60]
    content_preview.short_description = 'Content'
