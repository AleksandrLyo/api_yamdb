from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    CommentViewSet, ReviewViewSet, UserViewSet, signup,
                    user_activation)

app_name = 'api'

router = DefaultRouter()

router.register(
    'users',
    UserViewSet,
    basename='users'
)

router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments',
)
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', user_activation),
]
