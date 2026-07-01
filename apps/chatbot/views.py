from rest_framework import generics, permissions, status, serializers as drf_serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer, OpenApiExample

from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatSessionListSerializer, ChatMessageSerializer
from .services.ai_service import get_ai_response


# ─────────────────────────────────────────────
#  SHARED EXAMPLES
# ─────────────────────────────────────────────

_session_list_example = {
    "id": 1,
    "title": "Blog post ideas",
    "message_count": 4,
    "created_at": "2026-07-01T09:00:00Z",
    "updated_at": "2026-07-01T09:05:00Z",
}

_session_detail_example = {
    "id": 1,
    "title": "Blog post ideas",
    "message_count": 2,
    "messages": [
        {"id": 1, "role": "user",      "content": "Give me 3 blog post ideas about Django.", "created_at": "2026-07-01T09:00:00Z"},
        {"id": 2, "role": "assistant", "content": "Here are 3 ideas:\n1. ...\n2. ...\n3. ...", "created_at": "2026-07-01T09:00:01Z"},
    ],
    "created_at": "2026-07-01T09:00:00Z",
    "updated_at": "2026-07-01T09:00:01Z",
}

_message_example = {
    "id": 1,
    "role": "user",
    "content": "Give me 3 blog post ideas about Django.",
    "created_at": "2026-07-01T09:00:00Z",
}

_send_response_example = {
    "session_id": 1,
    "session_title": "Give me 3 blog post ideas about Django.",
    "user_message": {
        "id": 3,
        "role": "user",
        "content": "Give me 3 blog post ideas about Django.",
        "created_at": "2026-07-01T09:10:00Z",
    },
    "ai_reply": {
        "id": 4,
        "role": "assistant",
        "content": "Here are 3 blog post ideas about Django:\n\n1. **Getting Started with Django REST Framework**\n2. **Django ORM Deep Dive**\n3. **Deploying Django to Production**",
        "created_at": "2026-07-01T09:10:01Z",
    },
}


# ─────────────────────────────────────────────
#  CHAT SESSIONS
# ─────────────────────────────────────────────

@extend_schema_view(
    get=extend_schema(
        tags=["Chatbot"],
        summary="List chat sessions",
        description="Returns all chat sessions for the authenticated user, ordered by most recently updated.",
        operation_id="chatbot_session_list",
        examples=[
            OpenApiExample("Response", value=[_session_list_example], response_only=True, status_codes=["200"]),
        ],
    ),
    post=extend_schema(
        tags=["Chatbot"],
        summary="Create a chat session",
        description="Creates a new empty chat session. Optionally provide a `title`; defaults to **New Chat**.",
        operation_id="chatbot_session_create",
        examples=[
            OpenApiExample("Request", value={"title": "Blog post ideas"}, request_only=True),
            OpenApiExample("Response", value=_session_detail_example, response_only=True, status_codes=["201"]),
        ],
    ),
)
class ChatSessionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatSessionSerializer
        return ChatSessionListSerializer

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        tags=["Chatbot"],
        summary="Get session with full chat history",
        description="Returns the session details and all messages in chronological order.",
        operation_id="chatbot_session_retrieve",
        examples=[
            OpenApiExample("Response", value=_session_detail_example, response_only=True, status_codes=["200"]),
        ],
    ),
    patch=extend_schema(
        tags=["Chatbot"],
        summary="Rename a chat session",
        description="Update the `title` of an existing session.",
        operation_id="chatbot_session_update",
        examples=[
            OpenApiExample("Request", value={"title": "My renamed session"}, request_only=True),
            OpenApiExample("Response", value={**_session_detail_example, "title": "My renamed session"}, response_only=True, status_codes=["200"]),
        ],
    ),
    put=extend_schema(exclude=True),
    delete=extend_schema(
        tags=["Chatbot"],
        summary="Delete a chat session",
        description="Permanently deletes the session and all its messages.",
        operation_id="chatbot_session_delete",
    ),
)
class ChatSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user).prefetch_related('messages')


# ─────────────────────────────────────────────
#  MESSAGES
# ─────────────────────────────────────────────

@extend_schema(
    tags=["Chatbot"],
    summary="Get all messages in a session",
    description="Returns every message in the session in chronological order. Each message has a `role` of `user` or `assistant`.",
    operation_id="chatbot_message_list",
    examples=[
        OpenApiExample(
            "Response",
            value=[
                {"id": 1, "role": "user",      "content": "Give me 3 blog post ideas.", "created_at": "2026-07-01T09:00:00Z"},
                {"id": 2, "role": "assistant", "content": "Here are 3 ideas:\n1. ...",  "created_at": "2026-07-01T09:00:01Z"},
            ],
            response_only=True,
            status_codes=["200"],
        ),
    ],
)
class ChatMessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        return ChatMessage.objects.filter(
            session__id=session_id,
            session__user=self.request.user
        )


@extend_schema(
    tags=["Chatbot"],
    summary="Send a message — receive AI reply",
    description=(
        "Send a message to the AI within a specific chat session.\n\n"
        "The full conversation history is included with every request so the AI maintains context. "
        "The session title is automatically set from the first message if it has not been renamed."
    ),
    operation_id="chatbot_send_message",
    request=inline_serializer(
        name="SendMessageRequest",
        fields={"message": drf_serializers.CharField(help_text="The message to send to the AI.")},
    ),
    responses={
        201: inline_serializer(
            name="SendMessageResponse",
            fields={
                "session_id":    drf_serializers.IntegerField(),
                "session_title": drf_serializers.CharField(),
                "user_message":  ChatMessageSerializer(),
                "ai_reply":      ChatMessageSerializer(),
            },
        ),
        400: inline_serializer(
            name="SendMessageBadRequest",
            fields={"detail": drf_serializers.CharField()},
        ),
        503: inline_serializer(
            name="AIServiceUnavailable",
            fields={"detail": drf_serializers.CharField()},
        ),
    },
    examples=[
        OpenApiExample(
            "Request",
            value={"message": "Give me 3 blog post ideas about Django."},
            request_only=True,
        ),
        OpenApiExample(
            "Response",
            value=_send_response_example,
            response_only=True,
            status_codes=["201"],
        ),
    ],
)
class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
        except ChatSession.DoesNotExist:
            return Response({"detail": "Session not found."}, status=status.HTTP_404_NOT_FOUND)

        user_content = request.data.get('message', '').strip()
        if not user_content:
            return Response({"detail": "message is required."}, status=status.HTTP_400_BAD_REQUEST)

        user_msg = ChatMessage.objects.create(session=session, role='user', content=user_content)

        if session.title == "New Chat" and session.messages.count() == 1:
            session.title = user_content[:60]
            session.save(update_fields=['title'])

        try:
            ai_content = get_ai_response(session, user_content)
        except RuntimeError as exc:
            user_msg.delete()
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        ai_msg = ChatMessage.objects.create(session=session, role='assistant', content=ai_content)

        return Response({
            "session_id":    session.id,
            "session_title": session.title,
            "user_message":  ChatMessageSerializer(user_msg).data,
            "ai_reply":      ChatMessageSerializer(ai_msg).data,
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Chatbot"],
    summary="Clear all messages in a session",
    description="Deletes all messages in a session without removing the session itself. The title resets to **New Chat**.",
    operation_id="chatbot_session_clear",
    responses={
        200: inline_serializer(
            name="ClearSessionResponse",
            fields={"detail": drf_serializers.CharField()},
        ),
    },
    examples=[
        OpenApiExample(
            "Response",
            value={"detail": "Cleared 6 messages."},
            response_only=True,
            status_codes=["200"],
        ),
    ],
)
class ClearSessionView(APIView):
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
