from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError


from recipes.models import Recipe, Tag, Ingredient, Subscription, RecipeIngredient
from .constants import SHORT_LINK_PREFIX, DOMAIN
from .filters import RecipeFilter
from .serializers import (
    AdvancedUserSerializer, RecipeSerializer, RecipeCreateSerializer,
    TagSerializer, IngredientSerializer, ShortRecipeSerializer,
    SubscriptionUserSerializer, AvatarSerializer
)
from .permissions import IsAuthorOrAdminOrReadOnly

User = get_user_model()


class AvatarView(APIView):
    """Представление для добавления и удаления аватара пользователя."""

    permission_classes = [IsAuthenticated,]

    def put(self, request):
        user = request.user
        serializer = AvatarSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user.avatar = serializer.validated_data['avatar']
        user.save()
        return Response({'avatar': f'{DOMAIN}{user.avatar.url}'})  # ???

    def delete(self, request):
        user = request.user
        user.avatar = None
        user.save(update_fields=['avatar'])
        return Response(
            {'detail': 'Аватар успешно удалён'},
            status=status.HTTP_204_NO_CONTENT
        )


class SubscribeView(APIView):
    """Представление подписки на пользователя."""

    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return get_object_or_404(User, id=self.kwargs.get('id'))

    def post(self, request, *args, **kwargs):
        user = request.user
        follower = self.get_queryset()
        if (user == follower
            or Subscription.objects.filter(user=user, following=follower).exists()):
            raise ValidationError('Ошибка подписки')
        Subscription.objects.create(user=user, following=follower)
        serializer = SubscriptionUserSerializer(
            follower,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user = request.user
        follower = self.get_queryset()
        if not Subscription.objects.filter(user=user, following=follower).exists():
            raise ValidationError('Ошибка отписки')
        Subscription.objects.filter(user=user, following=follower).delete()
        return Response(
            {'detail': 'Успешная отписка'},
            status=status.HTTP_204_NO_CONTENT
        )


class SubscriptionsView(generics.ListAPIView):
    """Показывает список подписок."""

    serializer_class = SubscriptionUserSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(followers__user=user)


class RecipeViewSet(viewsets.ModelViewSet):
    """Предстваление отображения рецепта."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Recipe.objects.all().order_by('name')
    lookup_field = 'pk'
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        author_param = self.request.query_params.get('author', None)
        tags_param = self.request.query_params.getlist('tags', None)
        is_favorited_param = self.request.query_params.get('is_favorited', None)
        in_shopping_cart_param = self.request.query_params.get(
            'is_in_shopping_cart', None
        )
        if tags_param:
            queryset = queryset.filter(tags__slug__in=tags_param)

        if author_param:
            queryset = queryset.filter(author__id=author_param)

        if is_favorited_param == '1' and user.is_authenticated:
            queryset = queryset.filter(is_favorited=user)

        if in_shopping_cart_param == '1' and user.is_authenticated:
            queryset = queryset.filter(is_in_shopping_cart=user)
        return queryset.distinct()

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        read_serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        read_serializer = RecipeSerializer(recipe, context={'request': request})
        return Response(read_serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
    )
    def favorite(self, request, pk=None):
        """Добавляет и удаляет рецепт из избранного."""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = ShortRecipeSerializer(recipe, context={'request': request})

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
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Выгружает список покупок пользователю."""
        user = request.user
        users_recipes_in_cart = Recipe.objects.filter(
            is_in_shopping_cart=user
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
    )
    def shopping_cart(self, request, pk=None):  # весь метод в функцию?
        """Добавляет и удаляет рецепты из списка покупок."""
        user = request.user  # убрать в функцию
        recipe = get_object_or_404(Recipe, id=pk)
        recipes_in_cart = Recipe.objects.filter(is_in_shopping_cart=user)

        if request.method == 'POST':

            if recipe in recipes_in_cart:
                raise ValidationError(
                    'Ошибка добавления в список покупок'
                )
            recipe.is_in_shopping_cart.add(user)
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if recipe not in recipes_in_cart:
                raise ValidationError(
                    'Ошибка удаления из списка покупок'
                )

        recipe.is_in_shopping_cart.remove(user)
        return Response(
            {'detail': 'Рецепт успешно удалён из списка покупок'},
            status=status.HTTP_204_NO_CONTENT
        )

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


class DecodeLinkView(APIView):
    """С короткой ссылки перенаправляет на рецепт."""

    permission_classes = [AllowAny,]

    def get(self, request, hex_id=None):
        recipe_id = int(hex_id, base=16)
        recipe_url = reverse('recipe-detail', kwargs={'pk': recipe_id})
        return redirect(recipe_url)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление отображения тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny,]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление отображения тегов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny,]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('name',)
    search_fields = ('^name',)
