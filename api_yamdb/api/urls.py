"""Эндпойнты для приложения API."""

from django.urls import include, path
from rest_framework import routers

from api.views import (APIGetToken,
                       APISignup,
                       CategoryViewSet,
                       CommentViewSet,
                       GenreViewSet,
                       ReviewViewSet,
                       TitleViewSet,
                       UsersViewSet)

app_name = 'api'

router_version_1 = routers.DefaultRouter()
router_version_1.register('titles', TitleViewSet, basename='titles')
router_version_1.register('genres', GenreViewSet, basename='genres')
router_version_1.register(
    'categories', CategoryViewSet, basename='categories')
router_version_1.register('users', UsersViewSet, basename='users'),
router_version_1.register(r'titles/(?P<title_id>\d+)/reviews',
                          ReviewViewSet, basename='reviews')
router_version_1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

auth_urls = [
    path('token/', APIGetToken.as_view(), name='get_token'),
    path('signup/', APISignup.as_view(), name='signup'),
]

urlpatterns = [
    path('v1/', include(router_version_1.urls)),
    path('v1/auth/', include((auth_urls, 'auth'))),
]
