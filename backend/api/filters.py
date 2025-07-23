import django_filters
from django_filters import filters
from django_filters.rest_framework import FilterSet, AllValuesMultipleFilter, ModelMultipleChoiceFilter, BooleanFilter

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    """Настройка фильтрации рецептов."""

    def __init__(self, *a, **kw):
        print("RecipeFilter constructed")
        super().__init__(*a, **kw)

    tags = ModelMultipleChoiceFilter(queryset=Tag.objects.all(), field_name='tags__slug', to_field_name='slug')
    is_in_shopping_cart = BooleanFilter(
        method='filter_in_shopping_cart'
    )
    is_favorited = BooleanFilter(method='filter_is_favorited')

    class Meta:
        model = Recipe
        fields = ('author', 'tags__slug', 'is_favorited', 'is_in_shopping_cart')

    def filter_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        if value:
            return queryset.filter(is_in_shopping_cart=user)
        return queryset
    
    def filter_is_favorited(self, queryset, name, value):
        print('filter_is_favorited called')
        print(value)
        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()
        if value:
            return queryset.filter(is_favorited=user)
        return queryset.exclude(is_favorited=user)
