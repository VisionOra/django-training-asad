from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


@extend_schema(tags=["Accounts"])
class RegisterView(generics.CreateAPIView):
    #work
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=["Accounts"])
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
