from django.contrib import admin

from .models import Ingredient, Recipe, Subscription, Tag

admin.site.empty_value_display = 'Не задано'

admin.site.register(Tag)
admin.site.register(Subscription)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites_count')
    search_fields = ('author', 'name')
    list_filter = ('tags',)
    readonly_fields = ('favorites_count',)

    def favorites_count(self, obj):
        return obj.is_favorited.count()

    favorites_count.short_description = 'Количество добавлений в избранное'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
