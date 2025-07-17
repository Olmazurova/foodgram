from pprint import pprint

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, generics
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe, Tag, Ingredient, Subscription
from .serializers import (
    AdvancedUserSerializer, RecipeSerializer, RecipeCreateSerializer,
    TagSerializer, IngredientSerializer, ShortRecipeSerializer, SubscriptionUserSerializer)

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
            {'detail': 'Аватар успешно удалён'},
            status=status.HTTP_204_NO_CONTENT
        )


class SubscribeView(generics.CreateAPIView, generics.DestroyAPIView):
    """Представление подписки на пользователя."""

    permission_classes = [IsAuthenticated,]
    serializer_class = SubscriptionUserSerializer

    def get_queryset(self):
        return get_object_or_404(User, id=self.kwargs.get('id'))

    def create(self, request, *args, **kwargs):
        user = request.user
        follower = self.get_queryset()
        Subscription.objects.create(user=user, following=follower)
        serializer = self.get_serializer(
            follower,
            context={'request': request},
        )
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        user = request.user
        follower = self.get_queryset()
        Subscription.objects.filter(user=user, following=follower).delete()
        return Response(
            {'detail': 'Успешная отписка'},
            status=status.HTTP_204_NO_CONTENT
        )


class SubscriptionsView(generics.ListAPIView):
    """Показывает список подписок."""

    serializer_class = SubscriptionUserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(followers__user=user)



class RecipeViewSet(viewsets.ModelViewSet):
    """Предстваление отображения рецепта."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Recipe.objects.all()
    # serializer_class = RecipeSerializer
    # Доступна фильтрация по избранному, автору, списку покупок и тегам.
    # permissions - на чтение всем, создание - юзер, изменение-удаление - автор\адми

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        read_serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(read_serializer.data)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        read_serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(read_serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        """Добавляет и удаляет рецепт из избранного."""
        user = request.user
        recipe = Recipe.objects.get(id=pk)

        if request.method == 'POST':
            recipe.favorited.add(user)
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data)

        recipe.favorited.remove(user)

        return Response(
            {'detail': 'Рецепт успешно удалён из избранного'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Выгружает список покупок пользователю."""
        pass

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):  # весь метод в функцию?
        """Добавляет и удаляет рецепты из списка покупок."""
        user = request.user  # убрать в функцию
        recipe = Recipe.objects.get(id=pk)

        if request.method == 'POST':
            recipe.in_shopping_cart.add(user)
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data)

        recipe.in_shopping_cart.remove(user)
        return Response(
            {'detail': 'Рецепт успешно удалён из списка покупок'},
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
