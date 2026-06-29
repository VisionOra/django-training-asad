from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Blog app
    path('', include('apps.blog.urls')),

    # Accounts app
    path('accounts/', include('apps.accounts.urls')),

    # Built-in Django auth URLs: login/logout/password reset names
    path('accounts/', include('django.contrib.auth.urls')),

    # Swagger / schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]