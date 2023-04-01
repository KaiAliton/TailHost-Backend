from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.auth.auth import RegisterViewSet, LoginViewSet, RefreshViewSet
from api.v1.post.views import PostViewSet
from api.v1.user.views import UserViewSet

router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'post', PostViewSet, basename='post')
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
