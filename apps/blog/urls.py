from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='api-post')
router.register(r'categories', views.CategoryViewSet, basename='api-category')

urlpatterns = [
    # HTML pages (read only)
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    # API routes
    path('api/', include(router.urls)),
]