from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .constants import (
    MAX_LENGTH_TAG, MAX_LENGTH_INGREDIENT_NAME,
    MAX_LENGTH_INGREDIENT_UNIT, MAX_LENGTH_RECIPE,
    MAX_DIGITS, DECIMAL_PLACES
)

User = get_user_model()


class Tag(models.Model):
    """Модель описывающая теги."""

    name = models.CharField(
        max_length=MAX_LENGTH_TAG, unique=True, verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_TAG, unique=True, verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель описывающая ингредиенты рецептов."""

    name = models.CharField(
        max_length=MAX_LENGTH_INGREDIENT_NAME,
        unique=True,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_INGREDIENT_UNIT,
        verbose_name='Единица измерения'
    )
    amount = models.DecimalField(
        verbose_name='количество',
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель описывающая рецепт."""

    tags = models.ManyToManyField(
        Tag, related_name='recipe', verbose_name='теги'
    )
    author = models.ForeignKey(
        User, verbose_name='автор', on_delete=models.CASCADE
    )
    ingredients = models.ForeignKey(
        Ingredient, verbose_name='ингредиенты', on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=MAX_LENGTH_RECIPE, verbose_name='название'
    )
    image = models.ImageField(
        verbose_name='изображение', help_text='Загрузите изображение блюда'
    )
    text = models.TextField(
        verbose_name='описание',
        help_text='Заполните описание приготовления блюда'
    )
    cooking_time = models.SmallIntegerField(
        validators=[MinValueValidator(1),],
        verbose_name='время приготовления',
        help_text='Укажите время приготовления в минутах'
    )
    # is_favorited = bool - находится в избранном (сериализатор)
    # is_in_shopping_cart = bool - находится в списке покупок (сериализатор)

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    """Модель описывающая список покупок."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        related_name='shopping_cart',
        on_delete=models.DO_NOTHING
    )
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        related_name='shopping_cart',
        on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'
        unique_together = ('recipe', 'user')

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Favorites(models.Model):
    """Модель описывающая раздел "Избранное" пользователя."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='рецепт',
        related_name='favorites',
        on_delete=models.DO_NOTHING,
    )
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        related_name='favorites',
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('recipe', 'user')

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Subscription(models.Model):
    """Модель описывающая подписку пользователя на авторов."""

    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        related_name='subscription',
        on_delete=models.DO_NOTHING,
    )
    following = models.ForeignKey(
        User,
        verbose_name='подписка',
        related_name='follower',
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'following')

    def __str__(self):
        return f'{self.user} - {self.following}'
