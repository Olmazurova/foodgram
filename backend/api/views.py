from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe, Tag, Ingredient
from .serializers import (
    AdvancedUserSerializer, RecipeSerializer, RecipeCreateSerializer,
    TagSerializer, IngredientSerializer)

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
