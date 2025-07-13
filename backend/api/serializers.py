import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import (
    Subscription, Recipe, Ingredient, RecipeIngredient, Favorites,
    ShoppingCart, RecipeIngredient, Tag
)

User = get_user_model()


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        user = self.context['request'].user
        if self.context['request'].method == 'PUT':
            name = f'{user}.'
        else:
            recipe = Recipe.objects.get(id=self.context['request']['id'])
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

    pass


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    pass


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в рецепте с указанием их количества."""

    pass


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    tag = TagSerializer(many=True, read_only=True) # для записи здесь должно быть поле выбора?
    author = AdvancedUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):  # создать отдельную функцию для этих методов
        request = self.context.get('request')
        user = request.user
        return Favorites.objects.filter(user=user, recipe=obj).exists()

    def get_is_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания и обновления рецепта."""

    ingredients = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), many=True
    )
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
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            RecipeIngredient.objects.create(
                id_ingredient=current_ingredient,
                id_recipe=recipe,
                amount=ingredient['amount'],
            )
        return recipe

    def update(self, instance, validated_data):
        instance.tags = validated_data.get('tags', instance.tags)
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        if 'ingredients' not in validated_data:
            instance.save()
            return instance

        ingredients_data = validated_data.pop('ingredients')
        ingredients_update = []
        for ingredient in ingredients_data:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])  # можно ли вынести в отдельную функцию?
            RecipeIngredient.objects.create(
                id_ingredient=current_ingredient,
                id_recipe=instance,
                amount=ingredient['amount'],
            )
            ingredients_update.append(current_ingredient)
        instance.ingredients.set(ingredients_update)
        instance.save()
        return instance

    def validate_image(self, value):
        request = self.context.get('request')
        if request.method == 'POST' and value is None:
            raise serializers.ValidationError('Поле image не может быть пустым!')
        return value
