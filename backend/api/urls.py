from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .constants import SHORT_LINK_PREFIX
from .views import (
    AvatarView, TagViewSet, IngredientViewSet, RecipeViewSet, SubscribeView,
    SubscriptionsView
)

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)


urlpatterns = [
    path('users/me/avatar/', AvatarView.as_view(), name='avatar'),
    path('users/subscriptions/', SubscriptionsView.as_view(), name='subscriptions'),
    re_path(
        r'users/(?P<id>\d+)/subscribe/',
        SubscribeView.as_view(),
        name='subscribe'
    ),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
