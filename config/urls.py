from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from api.auth.auth import RegisterViewSet, LoginViewSet, RefreshViewSet
from api.v1.album.views import AlbumViewSet
from api.v1.comment.views import CommentViewSet
from api.v1.genre.views import GenreViewSet
from api.v1.post.views import PostViewSet
from api.v1.track.views import TrackViewSet
from api.v1.user.views import UserViewSet

router = routers.SimpleRouter()
router.register(r'user', UserViewSet, basename='user')

router.register(r'post', PostViewSet, basename='post')
posts_router = routers.NestedSimpleRouter(router, r'post', lookup='post')
posts_router.register(r'comment', CommentViewSet, basename='post-comment')

router.register(r'album', AlbumViewSet, basename='album')
router.register(r'track', TrackViewSet, basename='track')
router.register(r'genre', GenreViewSet, basename='genre')
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(posts_router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
