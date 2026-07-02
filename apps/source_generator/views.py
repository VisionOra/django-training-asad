from rest_framework import generics, permissions, status, serializers as drf_serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer, OpenApiExample

from .models import SourceSearch, Source
from .serializers import SourceSearchSerializer, SourceSearchListSerializer, SourceSerializer
from .services.serper_service import fetch_sources


# ─────────────────────────────────────────────
#  SHARED EXAMPLES
# ─────────────────────────────────────────────

_source_example = {
    "id": 1,
    "title": "Django REST Framework — Official Docs",
    "link": "https://www.django-rest-framework.org/",
    "snippet": "Django REST framework is a powerful and flexible toolkit for building Web APIs.",
    "position": 1,
}

_search_list_example = {
    "id": 1,
    "topic": "Django REST Framework",
    "limit": 10,
    "source_count": 10,
    "created_at": "2026-07-01T10:00:00Z",
    "updated_at": "2026-07-01T10:00:00Z",
}

_search_detail_example = {
    "id": 1,
    "topic": "Django REST Framework",
    "limit": 3,
    "source_count": 3,
    "sources": [
        {"id": 1, "title": "Django REST Framework — Official Docs", "link": "https://www.django-rest-framework.org/", "snippet": "A powerful toolkit for building Web APIs.", "position": 1},
        {"id": 2, "title": "DRF Tutorial", "link": "https://www.django-rest-framework.org/tutorial/1-serialization/", "snippet": "Step-by-step tutorial.", "position": 2},
        {"id": 3, "title": "DRF GitHub", "link": "https://github.com/encode/django-rest-framework", "snippet": "Source code on GitHub.", "position": 3},
    ],
    "created_at": "2026-07-01T10:00:00Z",
    "updated_at": "2026-07-01T10:00:00Z",
}


# ─────────────────────────────────────────────
#  SEARCHES
# ─────────────────────────────────────────────

@extend_schema_view(
    get=extend_schema(
        tags=["Source Generator"],
        summary="List all searches",
        description="Returns all source searches made by the authenticated user, ordered by most recent.",
        examples=[
            OpenApiExample("Response", value=[_search_list_example], response_only=True, status_codes=["200"]),
        ],
    ),
    post=extend_schema(
        tags=["Source Generator"],
        summary="Generate sources for a topic",
        description=(
            "Submit a topic to fetch authentic sources from the Serper (Google Search) API. "
            "Pass an optional `limit` to control how many sources are returned (default: 10). "
            "Results are saved to the database and returned immediately."
        ),
        examples=[
            OpenApiExample("Request", value={"topic": "Django REST Framework", "limit": 5}, request_only=True),
            OpenApiExample("Response", value=_search_detail_example, response_only=True, status_codes=["201"]),
        ],
    ),
)
class SourceSearchListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SourceSearchSerializer
        return SourceSearchListSerializer

    def get_queryset(self):
        return SourceSearch.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        topic = serializer.validated_data['topic']
        limit = serializer.validated_data.get('limit', 10)

        try:
            results = fetch_sources(topic, limit)
        except RuntimeError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        search = SourceSearch.objects.create(user=request.user, topic=topic, limit=limit)

        Source.objects.bulk_create([
            Source(
                search=search,
                title=r['title'],
                link=r['link'],
                snippet=r['snippet'],
                position=r['position'],
            )
            for r in results
        ])

        return Response(SourceSearchSerializer(search).data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        tags=["Source Generator"],
        summary="Get a search with all its sources",
        description="Returns the full search record including every fetched source.",
        examples=[
            OpenApiExample("Response", value=_search_detail_example, response_only=True, status_codes=["200"]),
        ],
    ),
    patch=extend_schema(
        tags=["Source Generator"],
        summary="Update search topic or limit",
        description="Update the `topic` or `limit` of an existing search. Does not re-fetch sources.",
        examples=[
            OpenApiExample("Request", value={"topic": "Django Signals"}, request_only=True),
        ],
    ),
    put=extend_schema(exclude=True),
    delete=extend_schema(
        tags=["Source Generator"],
        summary="Delete a search",
        description="Permanently deletes the search and all its associated sources.",
    ),
)
class SourceSearchDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SourceSearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SourceSearch.objects.filter(user=self.request.user).prefetch_related('sources')


# ─────────────────────────────────────────────
#  SOURCES
# ─────────────────────────────────────────────

@extend_schema(
    tags=["Source Generator"],
    summary="List sources for a search",
    description="Returns all sources saved under a specific search, ordered by position.",
    examples=[
        OpenApiExample("Response", value=[_source_example], response_only=True, status_codes=["200"]),
    ],
)
class SourceListView(generics.ListAPIView):
    serializer_class = SourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        search_id = self.kwargs['search_id']
        return Source.objects.filter(
            search__id=search_id,
            search__user=self.request.user,
        )


@extend_schema_view(
    get=extend_schema(
        tags=["Source Generator"],
        summary="Retrieve a single source",
        description="Returns the details of a single source by ID.",
        examples=[
            OpenApiExample("Response", value=_source_example, response_only=True, status_codes=["200"]),
        ],
    ),
    patch=extend_schema(
        tags=["Source Generator"],
        summary="Update a single source",
        description="Update the `title`, `link`, or `snippet` of a single source.",
        examples=[
            OpenApiExample("Request", value={"title": "Updated Title", "snippet": "Updated snippet."}, request_only=True),
            OpenApiExample("Response", value=_source_example, response_only=True, status_codes=["200"]),
        ],
    ),
    put=extend_schema(exclude=True),
    delete=extend_schema(
        tags=["Source Generator"],
        summary="Delete a single source",
        description="Removes a single source without deleting the entire search.",
    ),
)
class SourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Source.objects.filter(search__user=self.request.user)


# ─────────────────────────────────────────────
#  RE-FETCH
# ─────────────────────────────────────────────

@extend_schema(
    tags=["Source Generator"],
    summary="Re-fetch sources for an existing search",
    description=(
        "Deletes all existing sources for this search, calls the Serper API again "
        "with the same topic and limit, and saves fresh results."
    ),
    request=None,
    responses={
        200: SourceSearchSerializer,
        404: inline_serializer(name="RefetchNotFound", fields={"detail": drf_serializers.CharField()}),
        503: inline_serializer(name="RefetchServiceError", fields={"detail": drf_serializers.CharField()}),
    },
    examples=[
        OpenApiExample("Response", value=_search_detail_example, response_only=True, status_codes=["200"]),
    ],
)
class SourceRefetchView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            search = SourceSearch.objects.get(pk=pk, user=request.user)
        except SourceSearch.DoesNotExist:
            return Response({"detail": "Search not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            results = fetch_sources(search.topic, search.limit)
        except RuntimeError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        search.sources.all().delete()

        Source.objects.bulk_create([
            Source(
                search=search,
                title=r['title'],
                link=r['link'],
                snippet=r['snippet'],
                position=r['position'],
            )
            for r in results
        ])

        return Response(SourceSearchSerializer(search).data, status=status.HTTP_200_OK)
