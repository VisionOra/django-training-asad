from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Blog app (HTML + API)
    path('', include('apps.blog.urls')),

    # JWT auth API endpoints (register, login, refresh, profile)
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/chat/', include('apps.chatbot.urls')),

    # Built-in Django auth URLs for session-based HTML views (login/logout/password reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # Swagger / schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)