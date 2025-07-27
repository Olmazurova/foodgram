from recipes.models import Recipe


def get_recipes_in_cart(user):
    return Recipe.objects.filter(is_in_shopping_cart=user)


def get_recipes_in_favorited(user):
    return Recipe.objects.filter(is_favorited=user)
