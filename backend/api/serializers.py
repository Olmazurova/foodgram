import base64
from pprint import pprint

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone
from rest_framework import serializers

from recipes.models import (
    Subscription, Recipe, Ingredient, RecipeIngredient, Tag
)

User = get_user_model()


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        user = self.context['request'].user
        if self.context['request'].method == 'PUT':
            name = f'{user}.'
        elif self.context['request'].method == 'POST':
            name = f'{user}-{timezone.now()}.'
        else:
            pprint(self.context['request'].id)
            recipe = Recipe.objects.get(id=self.context['request']['kwargs']['id'])
            name = f'{user}-{recipe}.'
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            file_extension = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=name + file_extension
            )
        return super().to_internal_value(data)


class AdvancedUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    is_subscribed = serializers.SerializerMethodField()
    avatar = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'avatar'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        return Subscription.objects.filter(user=user, following=obj).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), source='ingredient')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(source='ingredient.measurement_unit', read_only=True)
    amount = serializers.DecimalField(min_value=1, max_digits=5, decimal_places=2,)


    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    id =  serializers.IntegerField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = AdvancedUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True, read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):  # создать отдельную функцию для этих методов
        user = self.context.get('request').user
        return obj.favorited.filter(id=user.id).exists()

    def get_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return obj.in_shopping_cart.filter(id=user.id).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания и обновления рецепта."""

    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(required=False)  # в patch запросе необязателен

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        user = self.context.get('request').user
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients_data:
            print(ingredient)
            current_ingredient = ingredient['ingredient']
            amount = ingredient['amount']
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        print(ingredients_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.tags.set(tags)

        # RecipeIngredient.objects.filter(recipe=instance).delete()
        for ingredient in ingredients_data:
            current_ingredient = Ingredient.objects.get(id=ingredient['ingredient'])
            amount = ingredient['amount']
            RecipeIngredient.objects.update_or_create(
                ingredient=current_ingredient,
                recipe=instance,
                amount=amount
            )
        return instance

    def validate_image(self, value):
        request = self.context.get('request')
        if request.method == 'POST' and value is None:
            raise serializers.ValidationError('Поле image не может быть пустым!')
        return value


class FavoritesSerializer(serializers.ModelSerializer):
    """Сериализатор для раздела 'избранное'."""

    # name = serializers.StringRelatedField(source='name')
    # image = serializers.ImageField(source='image')
    # cooking_time = serializers.IntegerField(source='cooking_time')

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


# class ShoppingCartSerializer(serializers.ModelSerializer):
#     """Сериализатор для раздела 'избранное'."""
#
#     name = serializers.StringRelatedField(source='recipe__name')
#     image = serializers.ImageField(source='recipe__image')
#     cooking_time = serializers.IntegerField(source='recipe__cooking_time')
#
#     class Meta:
#         model = ShoppingCart
#         fields = ('id', 'name', 'image', 'cooking_time')