from rest_framework import generics, permissions, status, serializers as drf_serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer, OpenApiExample

from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatSessionListSerializer, ChatMessageSerializer
from .services.ai_service import get_ai_response


# ─────────────────────────────────────────────
#  CHAT SESSIONS
# ─────────────────────────────────────────────

@extend_schema_view(
    get=extend_schema(
        tags=["Chatbot"],
        summary="List all chat sessions",
        description="Returns all chat sessions belonging to the authenticated user, ordered by most recently updated.",
        operation_id="chatbot_session_list",
    ),
    post=extend_schema(
        tags=["Chatbot"],
        summary="Create a new chat session",
        description="Creates a new empty chat session for the authenticated user. Optionally provide a `title`; defaults to **New Chat**.",
        operation_id="chatbot_session_create",
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
        summary="Retrieve a chat session with full history",
        description="Returns the session details along with the complete message history in chronological order.",
        operation_id="chatbot_session_retrieve",
    ),
    patch=extend_schema(
        tags=["Chatbot"],
        summary="Rename a chat session",
        description="Update the `title` of an existing session.",
        operation_id="chatbot_session_update",
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
    summary="Get chat history",
    description="Returns all messages in a session in chronological order. Each message has a `role` of **user** or **assistant**.",
    operation_id="chatbot_message_list",
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
    summary="Send a message and get AI reply",
    description=(
        "Send a message to the AI inside a specific chat session.\n\n"
        "- The user message is saved first\n"
        "- Full conversation history is sent to the AI for context\n"
        "- Both the user message and AI reply are returned\n"
        "- The session `title` is auto-set from the first message if it hasn't been renamed"
    ),
    operation_id="chatbot_send_message",
    request=inline_serializer(
        name="SendMessageRequest",
        fields={"message": drf_serializers.CharField(help_text="The message text to send to the AI")},
    ),
    responses={
        201: inline_serializer(
            name="SendMessageResponse",
            fields={
                "session_id": drf_serializers.IntegerField(),
                "session_title": drf_serializers.CharField(),
                "user_message": ChatMessageSerializer(),
                "ai_reply": ChatMessageSerializer(),
            },
        ),
        400: inline_serializer(
            name="SendMessageError",
            fields={"detail": drf_serializers.CharField()},
        ),
        503: inline_serializer(
            name="AIServiceError",
            fields={"detail": drf_serializers.CharField()},
        ),
    },
    examples=[
        OpenApiExample(
            "Send a message",
            value={"message": "Give me 3 blog post ideas about Python."},
            request_only=True,
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
            "session_id": session.id,
            "session_title": session.title,
            "user_message": ChatMessageSerializer(user_msg).data,
            "ai_reply": ChatMessageSerializer(ai_msg).data,
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Chatbot"],
    summary="Clear all messages in a session",
    description="Deletes all messages inside a session without deleting the session itself. The session title resets to **New Chat**.",
    operation_id="chatbot_session_clear",
    responses={
        200: inline_serializer(
            name="ClearSessionResponse",
            fields={"detail": drf_serializers.CharField()},
        ),
    },
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
