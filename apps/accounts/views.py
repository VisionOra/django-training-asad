from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


@extend_schema(
    tags=["Accounts"],
    summary="Register a new user",
    description="Create a new user account. Returns the username and email of the created user.",
    operation_id="accounts_register",
    examples=[
        OpenApiExample(
            "Register request",
            value={
                "username": "john_doe",
                "email": "john@example.com",
                "password": "StrongPass123",
                "password2": "StrongPass123",
            },
            request_only=True,
        ),
        OpenApiExample(
            "Register response",
            value={"username": "john_doe", "email": "john@example.com"},
            response_only=True,
            status_codes=["201"],
        ),
    ],
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    tags=["Accounts"],
    summary="Get current user profile",
    description="Returns the profile of the currently authenticated user.",
    operation_id="accounts_profile",
    examples=[
        OpenApiExample(
            "Profile response",
            value={"id": 1, "username": "john_doe", "email": "john@example.com"},
            response_only=True,
            status_codes=["200"],
        ),
    ],
)
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
