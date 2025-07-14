from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, generics
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from recipes.models import Recipe, Tag, Ingredient, Favorites, ShoppingCart
from .serializers import (
    AdvancedUserSerializer, RecipeSerializer, RecipeCreateSerializer,
    TagSerializer, IngredientSerializer, FavoritesSerializer,
    ShoppingCartSerializer)

User = get_user_model()


class AvatarView(APIView):
    """Представление для добавления и удаления аватара пользователя."""

    def put(self, request):
        user = request.user
        serializer = AdvancedUserSerializer(
            user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        user.avatar = None
        user.save(update_fields=['avatar'])
        return Response(
            {'message': 'Аватар успешно удалён'},
            status=status.HTTP_204_NO_CONTENT
        )


class RecipeViewSet(viewsets.ModelViewSet):
    """Предстваление отображения рецепта."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Recipe.objects.all()
    # serializer_class = RecipeSerializer
    # Доступна фильтрация по избранному, автору, списку покупок и тегам.
    # permissions - на чтение всем, создание - юзер, изменение-удаление - автор\админ

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
        # url_path='id/favorite',
    )
    def favorite(self, request, id=None):
        """Добавляет и удаляет рецепт из избранного."""
        user = request.user
        recipe = Recipe.objects.get(id=id)

        if request.method == 'POST':
            result = Favorites.objects.create(user=user, recipe=recipe)
            serializer = FavoritesSerializer(result)
            return Response(serializer.data)

        result = get_object_or_404(Favorites, user=user, recipe=recipe)
        result.delete()
        return Response(
            {'detail': 'Рецепт успешно удалён из избранного'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Выгружает список покупок пользователю."""
        pass

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, id=None):  # весь метод в функцию?
        """Добавляет и удаляет рецепты из корзины покупок."""
        user = request.user  # убрать в функцию
        recipe = Recipe.objects.get(id=id)

        if request.method == 'POST':
            result = ShoppingCart.objects.create(user=user, recipe=recipe)
            serializer = ShoppingCartSerializer(result)
            return Response(serializer.data)

        result = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
        result.delete()
        return Response(
            {'detail': 'Рецепт успешно удалён из избранного'},
            status=status.HTTP_204_NO_CONTENT
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление отображения тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permissions


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление отображения тегов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # permissions



