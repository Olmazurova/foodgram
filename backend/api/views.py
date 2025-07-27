from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response

from .constants import DOMAIN, SHORT_LINK_PREFIX
from .filters import RecipeFilter
from .mixins import (AllowAnyPermissionsMixin, AuthenticatedPermissionMixin,
                     GetUserMixin, NonePaginationPermissionMixin)
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (AvatarSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          ShortRecipeSerializer, SubscriptionUserSerializer,
                          TagSerializer)
from .utils import get_recipes_in_cart
from recipes.models import (Ingredient, Recipe, RecipeIngredient, Subscription,
                            Tag)

User = get_user_model()


class AvatarView(AuthenticatedPermissionMixin):
    """Представление для добавления и удаления аватара пользователя."""

    def put(self, request):
        user = self.get_user()
        serializer = AvatarSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user.avatar = serializer.validated_data['avatar']
        user.save()
        return Response({'avatar': f'{DOMAIN}{user.avatar.url}'})

    def delete(self, request):
        user = self.get_user()
        user.avatar = None
        user.save(update_fields=['avatar'])
        return Response(
            {'detail': 'Аватар успешно удалён'},
            status=status.HTTP_204_NO_CONTENT
        )


class SubscribeView(AuthenticatedPermissionMixin):
    """Представление подписки на пользователя."""

    def get_queryset(self):
        return get_object_or_404(User, id=self.kwargs.get('id'))

    def post(self, request, *args, **kwargs):
        user = self.get_user()
        follower = self.get_queryset()
        if user == follower or Subscription.objects.filter(
                user=user, following=follower
        ).exists():
            raise ValidationError('Ошибка подписки')
        Subscription.objects.create(user=user, following=follower)
        serializer = SubscriptionUserSerializer(
            follower,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user = self.get_user()
        follower = self.get_queryset()
        if not Subscription.objects.filter(
                user=user, following=follower
        ).exists():
            raise ValidationError('Ошибка отписки')
        Subscription.objects.filter(user=user, following=follower).delete()
        return Response(
            {'detail': 'Успешная отписка'},
            status=status.HTTP_204_NO_CONTENT
        )


class SubscriptionsView(AuthenticatedPermissionMixin, generics.ListAPIView):
    """Показывает список подписок."""

    serializer_class = SubscriptionUserSerializer

    def get_queryset(self):
        return User.objects.filter(followers__user=self.get_user())


class RecipeViewSet(GetUserMixin, viewsets.ModelViewSet):
    """Предстваление отображения рецепта."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Recipe.objects.all().order_by('-created')
    lookup_field = 'pk'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthorOrAdminOrReadOnly()]

    def create(self, request, *args, **kwargs):
        return self._handler_recipe(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        return self._handler_recipe(request, update=True, *args, **kwargs)

    def _handler_recipe(self, request, update=False, *args, **kwargs):
        instance = self.get_object() if update else None
        serializer = self.get_serializer(
            instance, data=request.data, partial=update
        )
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        read_serializer = RecipeSerializer(
            recipe, context={'request': request}
        )
        response_status = (status.HTTP_200_OK if update
                           else status.HTTP_201_CREATED)
        return Response(read_serializer.data, status=response_status)

    @action(
        detail=True,
        methods=['post', 'delete'],
    )
    def favorite(self, request, pk=None):
        """Добавляет и удаляет рецепт из избранного."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = ShortRecipeSerializer(
            recipe, context={'request': request}
        )

        if request.method == 'POST':
            recipes_in_favorited = Recipe.objects.filter(is_favorited=user)
            if recipe in recipes_in_favorited:
                raise ValidationError(
                    'Ошибка добавления в избранное'
                )
            recipe.is_favorited.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            recipes_in_favorited = Recipe.objects.filter(is_favorited=user)
            if recipe not in recipes_in_favorited:
                raise ValidationError(
                    'Ошибка удаления из избранного'
                )
            recipe.is_favorited.remove(user)
        return Response(
            {'detail': 'Рецепт успешно удалён из избранного'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=True,
        methods=['post', 'delete'],
    )
    def shopping_cart(self, request, pk=None):
        """Добавляет и удаляет рецепт из избранного."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = ShortRecipeSerializer(
            recipe, context={'request': request}
        )
        recipes_in_shopping_cart = Recipe.objects.filter(
            is_in_shopping_cart=user
        )

        if request.method == 'POST':
            if recipe in recipes_in_shopping_cart:
                raise ValidationError(
                    'Ошибка добавления в список покупок'
                )
            recipe.is_in_shopping_cart.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if recipe not in recipes_in_shopping_cart:
                raise ValidationError(
                    'Ошибка удаления из списка покупок'
                )
            recipe.is_in_shopping_cart.remove(user)
        return Response(
            {'detail': 'Рецепт успешно удалён из списка покупок'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['get']
    )
    def download_shopping_cart(self, request):
        """Выгружает список покупок пользователю."""
        user = self.get_user()
        users_recipes_in_cart = get_recipes_in_cart(user).values_list(
            'id', flat=True
        )
        users_ingredients = RecipeIngredient.objects.filter(
            recipe__in=users_recipes_in_cart
        ).order_by('ingredient')
        ingredients_summary = users_ingredients.values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total_amount=Sum('amount'))
        file_name = f'shopping_cart_{user.username}.txt'
        content = ['Ваш список покупок:', ]

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
        methods=['get'],
        permission_classes=[AllowAny],
        url_path='get-link',
    )
    def get_link(self, request, pk=None):
        """Возвращает короткую ссылку на рецепт."""
        recipe = get_object_or_404(Recipe, id=pk)
        short_url = f'{SHORT_LINK_PREFIX}{hex(recipe.id)}/'
        return Response(
            {'short-link': short_url}, status=status.HTTP_200_OK
        )


class DecodeLinkView(AllowAnyPermissionsMixin):
    """С короткой ссылки перенаправляет на рецепт."""

    def get(self, request, hex_id=None):
        recipe_id = int(hex_id, base=16)
        recipe_url = reverse('recipe-detail', kwargs={'pk': recipe_id})
        return redirect(recipe_url)


class TagViewSet(NonePaginationPermissionMixin, viewsets.ReadOnlyModelViewSet):
    """Представление отображения тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(
    NonePaginationPermissionMixin, viewsets.ReadOnlyModelViewSet
):
    """Представление отображения тегов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('name',)
    search_fields = ('^name',)
