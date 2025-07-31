from recipes.models import Recipe, RecipeIngredient, Subscription


def get_recipes_filter_by_field_name(field_name, value):
    filter_kwargs = {field_name: value}
    return Recipe.objects.filter(**filter_kwargs)


def available_subscription(user, following):
    return Subscription.objects.filter(
        user=user, following=following
    ).exists()


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
