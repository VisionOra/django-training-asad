from rest_framework import serializers
from .models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'role', 'content', 'created_at')
        read_only_fields = ('id', 'role', 'created_at')


class ChatSessionListSerializer(serializers.ModelSerializer):
    """Lightweight — used for list endpoint (no messages payload)."""
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ('id', 'title', 'message_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_message_count(self, obj) -> int:
        return obj.messages.count()


class ChatSessionSerializer(serializers.ModelSerializer):
    """Full detail — includes all messages."""
    messages = ChatMessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ('id', 'title', 'message_count', 'messages', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_message_count(self, obj) -> int:
        return obj.messages.count()
