from django.urls import path
from .views import (
    SourceSearchListCreateView,
    SourceSearchDetailView,
    SourceListView,
    SourceDetailView,
    SourceRefetchView,
)

urlpatterns = [
    path('searches/',                          SourceSearchListCreateView.as_view(), name='source-search-list'),
    path('searches/<int:pk>/',                 SourceSearchDetailView.as_view(),     name='source-search-detail'),
    path('searches/<int:pk>/refetch/',         SourceRefetchView.as_view(),          name='source-refetch'),
    path('searches/<int:search_id>/sources/',  SourceListView.as_view(),             name='source-list'),
    path('sources/<int:pk>/',                  SourceDetailView.as_view(),           name='source-detail'),
]
