import os

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Recipe, Tag, Ingredient, Subscription, RecipeIngredient
from .constants import SHORT_LINK_PREFIX
from .serializers import (
    AdvancedUserSerializer, RecipeSerializer, RecipeCreateSerializer,
    TagSerializer, IngredientSerializer, ShortRecipeSerializer,
    SubscriptionUserSerializer
)

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
        return get_object_or_404(User, id=self.kwargs.get('pk'))

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
    lookup_field = 'pk'
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
        recipe = Recipe.objects.get(pk=id)

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
        user = request.user
        users_recipes_in_cart = Recipe.objects.filter(
            in_shopping_cart=user
        ).values_list('id', flat=True)
        users_ingredients = RecipeIngredient.objects.filter(
            recipe__in=users_recipes_in_cart
        ).order_by('ingredient')
        ingredients_summary = users_ingredients.values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total_amount=Sum('amount'))
        file_name = f'shopping_cart_{user.username}.txt'
        content = ['Ваш список покупок:',]

        for ingredient in ingredients_summary:
            name = ingredient['ingredient__name']
            measurement_init = ingredient['ingredient__measurement_unit']
            amount = ingredient['total_amount']
            content.append(f'{name} - {amount} {measurement_init}')

        file_content = '\n'.join(content)

        response = HttpResponse(
            file_content, content_type='text/plain; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response


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

    @action(
        detail=True,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        url_path='get-link',
    )
    def get_link(self, request, pk=None):
        """Возвращает короткую ссылку на рецепт."""
        recipe = Recipe.objects.get(id=pk)
        short_url = f'{SHORT_LINK_PREFIX}{hex(recipe.id)}/'
        return Response(
            {'short-link': short_url}, status=status.HTTP_200_OK
        )


class DecodeLinkView(APIView):
    """С короткой ссылки перенаправляет на рецепт."""

    def get(self, request, hex_id=None):
        recipe_id = int(hex_id, base=16)
        recipe_url = reverse('recipe-detail', kwargs={'pk': recipe_id})
        return redirect(recipe_url)


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
