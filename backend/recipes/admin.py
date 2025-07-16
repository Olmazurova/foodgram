from django.contrib import admin

from .models import (
    Recipe, Tag, Ingredient, Subscription
)

admin.site.empty_value_display = 'Не задано'

admin.site.register(Tag)
admin.site.register(Subscription)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('author', 'name')
    list_filter = ('tags',)
    # общее число добавлений в избранное


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
