from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Blog app (HTML + API)
    path('', include('apps.blog.urls')),

    # JWT auth API endpoints (register, login, refresh, profile)
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/chat/', include('apps.chatbot.urls')),

    # Built-in Django auth URLs for session-based HTML views
    path('accounts/', include('django.contrib.auth.urls')),

    # API schema + docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
