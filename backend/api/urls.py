from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AvatarView, TagViewSet, IngredientViewSet, RecipeViewSet

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/me/avatar/', AvatarView.as_view(), name='avatar'),
    path('', include(router.urls)),
]