from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import ShortRecipeSerializer


def get_recipes_in_cart(user):
    return Recipe.objects.filter(is_in_shopping_cart=user)


def get_recipes_in_favorited(user):
    return Recipe.objects.filter(is_favorited=user)


def _handler_favorite_or_cart(self, request, pk=None, cart=False):
    user = self.get_user()
    recipe = get_object_or_404(Recipe, id=pk)
    recipes_in_name_field = (get_recipes_in_cart(user) if cart
                             else get_recipes_in_favorited(user))
    print('qs', recipes_in_name_field)
    add_validation_message = 'список покупок' if cart else 'избранное'
    del_message = 'списка покупок' if cart else 'избранного'

    if request.method == 'POST':
        # if recipe in recipes_in_name_field:
        #     raise ValidationError(
        #         f'Ошибка добавления в {add_validation_message}'
        #     )
        if cart:
            recipe.is_in_shopping_cart.add(user)
        else:
            recipe.is_favorited.add(user)
        serializer = ShortRecipeSerializer(data=recipe,
                                           context={'request': request})
        serializer.is_valid()
        return Response(
            serializer.validated_data, status=status.HTTP_201_CREATED
        )

    if recipe not in recipes_in_name_field:
        raise ValidationError(
            f'Ошибка удаления из {del_message}'
        )
    if cart:
        recipe.is_in_shopping_cart.remove(user)
    else:
        recipe.is_favorited.remove(user)
    return Response(
        {'detail': f'Рецепт успешно удалён из {del_message}'},
        status=status.HTTP_204_NO_CONTENT
    )
