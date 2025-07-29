from django_filters.rest_framework import (BooleanFilter, FilterSet,
                                           ModelMultipleChoiceFilter)

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    """Настройка фильтрации рецептов."""

    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug'
    )
    is_in_shopping_cart = BooleanFilter(
        method='filter_in_shopping_cart'
    )
    is_favorited = BooleanFilter(method='filter_is_favorited')

    class Meta:
        model = Recipe
        fields = (
            'author', 'tags__slug', 'is_favorited', 'is_in_shopping_cart'
        )

    def _filter_user_relation(self, queryset,field_name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        filter_kwargs = {field_name: user}
        if value:
            return queryset.filter(**filter_kwargs)
        return queryset

    def filter_in_shopping_cart(self, queryset, name, value):
        return self._filter_user_relation(
            queryset,
            field_name='is_in_shopping_cart',
            value=value,
        )

    def filter_is_favorited(self, queryset, name, value):
        return self._filter_user_relation(
            queryset, field_name='is_favorited', value=value,
        )
