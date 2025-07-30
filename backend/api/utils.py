from recipes.models import Recipe, RecipeIngredient


def get_recipes_in_cart(user):
    return Recipe.objects.filter(is_in_shopping_cart=user)


def get_recipes_in_favorited(user):
    return Recipe.objects.filter(is_favorited=user)


def bulk_create_ingredients_and_tags(recipe, ingredients_data, tags):
    recipe.tags.set(tags)
    RecipeIngredient.objects.filter(recipe=recipe).delete()
    objs = RecipeIngredient.objects.bulk_create(
        RecipeIngredient(
            ingredient=ingredient['ingredient'],
            recipe=recipe,
            amount=ingredient['amount']
        )
        for ingredient in ingredients_data
    )
    return objs