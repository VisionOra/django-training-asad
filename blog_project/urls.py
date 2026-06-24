from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Django built-in login/logout pages
    path('accounts/', include('django.contrib.auth.urls')),

    # Blog app URLs
    path('', include('apps.blog.urls')),

    # Accounts / JWT API URLs
    path('api/accounts/', include('apps.accounts.urls')),

    # Swagger / schema URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]