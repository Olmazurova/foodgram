from django.contrib import admin

from .models import (
    Recipe, Tag, Ingredient, Favorites, Subscription, ShoppingCart
)

admin.site.empty_value_display = 'Не задано'

admin.site.register(Tag)
admin.site.register(Favorites)
admin.site.register(Subscription)
admin.site.register(ShoppingCart)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('author', 'name')
    list_filter = ('tag',)
    # общее число добавлений в избранное


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
