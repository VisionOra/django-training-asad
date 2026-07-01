from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers as drf_serializers

from .models import ChatSession, ChatMessage
from .serializers import (
    ChatSessionSerializer,
    ChatSessionListSerializer,
    ChatMessageSerializer,
)


@extend_schema(tags=["Chat Sessions"])
class ChatSessionListCreateView(generics.ListCreateAPIView):
    """GET = list my sessions (lightweight), POST = create a new session."""
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatSessionSerializer
        return ChatSessionListSerializer

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Chat Sessions"])
class ChatSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET = session with full message history, PATCH = rename, DELETE = remove."""
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).prefetch_related('messages')


@extend_schema(tags=["Messages"])
class ChatMessageListView(generics.ListAPIView):
    """GET all messages in one session."""
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        return ChatMessage.objects.filter(
            session__id=session_id,
            session__user=self.request.user
        )


@extend_schema(
    tags=["Messages"],
    request=inline_serializer(
        name="SendMessageRequest",
        fields={"content": drf_serializers.CharField()},
    ),
    responses={201: inline_serializer(
        name="SendMessageResponse",
        fields={
            "user_message": ChatMessageSerializer(),
            "ai_message": ChatMessageSerializer(),
            "session_title": drf_serializers.CharField(),
        },
    )},
)
class SendMessageView(APIView):
    """POST { content } -> saves user message, gets AI reply, returns both."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response(
                {"detail": "Session not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        user_content = request.data.get('content', '').strip()
        if not user_content:
            return Response(
                {"detail": "content is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_msg = ChatMessage.objects.create(
            session=session, role='user', content=user_content
        )

        # Auto-title the session from the first user message
        if session.title == "New Chat" and session.messages.count() == 1:
            session.title = user_content[:60]
            session.save(update_fields=['title'])

        from .langchain_service import get_ai_response
        try:
            ai_content = get_ai_response(session, user_content)
        except RuntimeError as exc:
            # Delete the user message we already saved so the session stays clean
            user_msg.delete()
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        ai_msg = ChatMessage.objects.create(
            session=session, role='assistant', content=ai_content
        )

        return Response({
            "user_message": ChatMessageSerializer(user_msg).data,
            "ai_message": ChatMessageSerializer(ai_msg).data,
            "session_title": session.title,
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Chat Sessions"],
    responses={200: inline_serializer(
        name="ClearSessionResponse",
        fields={"detail": drf_serializers.CharField()},
    )},
)
class ClearSessionView(APIView):
    """DELETE all messages in a session without deleting the session itself."""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({"detail": "Session not found."}, status=status.HTTP_404_NOT_FOUND)

        deleted_count, _ = session.messages.all().delete()
        session.title = "New Chat"
        session.save(update_fields=['title'])
        return Response({"detail": f"Cleared {deleted_count} messages."}, status=status.HTTP_200_OK)
