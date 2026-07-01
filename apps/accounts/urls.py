from django.urls import path
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserProfileView


class LoginView(TokenObtainPairView):
    @extend_schema(
        tags=["Accounts"],
        summary="Login — obtain JWT tokens",
        description=(
            "Authenticate with username and password. "
            "Returns an `access` token (valid 60 min) and a `refresh` token (valid 7 days)."
        ),
        operation_id="accounts_login",
        examples=[
            OpenApiExample(
                "Request",
                value={"username": "john_doe", "password": "StrongPass123"},
                request_only=True,
            ),
            OpenApiExample(
                "Response",
                value={
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshView(TokenRefreshView):
    @extend_schema(
        tags=["Accounts"],
        summary="Refresh access token",
        description="Exchange a valid `refresh` token for a new `access` token.",
        operation_id="accounts_token_refresh",
        examples=[
            OpenApiExample(
                "Request",
                value={"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
                request_only=True,
            ),
            OpenApiExample(
                "Response",
                value={"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
                response_only=True,
                status_codes=["200"],
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    LoginView.as_view(),    name='token_obtain_pair'),
    path('refresh/',  RefreshView.as_view(),  name='token_refresh'),
    path('profile/',  UserProfileView.as_view(), name='user_profile'),
]
