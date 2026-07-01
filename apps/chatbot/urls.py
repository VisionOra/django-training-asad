from django.urls import path
from .views import (
    ChatSessionListCreateView,
    ChatSessionDetailView,
    ChatMessageListView,
    SendMessageView,
    ClearSessionView,
)

urlpatterns = [
    path('sessions/', ChatSessionListCreateView.as_view(), name='session-list'),
    path('sessions/<int:pk>/', ChatSessionDetailView.as_view(), name='session-detail'),
    path('sessions/<int:session_id>/messages/', ChatMessageListView.as_view(), name='message-list'),
    path('sessions/<int:session_id>/message/', SendMessageView.as_view(), name='send-message'),
    path('sessions/<int:session_id>/clear/', ClearSessionView.as_view(), name='session-clear'),
]
