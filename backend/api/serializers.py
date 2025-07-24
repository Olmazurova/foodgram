import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils import timezone
from rest_framework import serializers

from recipes.models import (
    Subscription, Recipe, Ingredient, RecipeIngredient, Tag
)
from .constants import PAGE_SIZE

User = get_user_model()


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        user = self.context['request'].user
        if self.context['request'].method == 'PUT':
            name = f'{user}.'
        elif self.context['request'].method == 'POST':
            name = f'{user}-{timezone.now()}.'
        else:
            id = self.context['request'].path.split('/')[-2]
            recipe = Recipe.objects.get(id=int(id))
            name = f'{user}-{recipe}.'
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            file_extension = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=name + file_extension
            )
        return super().to_internal_value(data)


class AvatarSerializer(serializers.Serializer):
    """Сериализует аватар пользователя."""

    avatar = Base64ImageField()

    class Meta:
        fields = ('avatar',)


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
        user = self.context.get('request').user
        if user.is_authenticated:
            return Subscription.objects.filter(
                user=user, following=obj
            ).exists()
        return False


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password',
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

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
    )
    name = serializers.CharField(
        source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )
    amount = serializers.IntegerField(min_value=1)

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
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time',
        )

    def get_is_favorited(self, obj):  # создать отдельную функцию для этих методов
        user = self.context.get('request').user
        return (user.is_authenticated
                and obj.is_favorited.filter(id=user.id).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated
                and obj.is_in_shopping_cart.filter(id=user.id).exists())


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания и обновления рецепта."""

    ingredients = RecipeIngredientSerializer(
        many=True, source='recipeingredient_set'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()  # в patch запросе необязателен

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time',
        )

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        tags = validated_data.pop('tags')
        user = self.context.get('request').user
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients_data:
            current_ingredient = ingredient['ingredient']
            amount = ingredient['amount']
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        ingredients_data = validated_data.pop('recipeingredient_set', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        for ingredient in ingredients_data:
            current_ingredient = Ingredient.objects.get(
                id=ingredient['ingredient'].id
            )
            amount = ingredient['amount']
            RecipeIngredient.objects.create(
                ingredient=current_ingredient,
                recipe=instance,
                amount=amount
            )
        return instance

    def validate_image(self, value):
        request = self.context.get('request')
        if request.method == 'POST' and value is None:
            raise serializers.ValidationError('Обязательное поле.')
        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError("Обязательное поле.")
        ingredient_ids = [ingredient['ingredient'].id for ingredient in value]
        if len(ingredient_ids) != len(set(ingredient_ids)):
            raise serializers.ValidationError(
                'Нельзя добавлять одинаковые ингредиенты в рецепт.')
        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError('Обязательное поле.')
        tags_ids = [tags.id for tags in value]
        if len(tags_ids) != len(set(tags_ids)):
            raise serializers.ValidationError(
                'Нельзя добавлять одинаковые теги в рецепт.')
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method == 'PATCH':
            missing_fields = []
            for field in ['recipeingredient_set', 'tags', 'name', 'text',
                          'cooking_time']:
                if field not in attrs:
                    missing_fields.append(field)
            if missing_fields:
                raise serializers.ValidationError(
                    {field: 'Обязательное поле.' for field in
                     missing_fields}
                )
        return attrs


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для раздела 'избранное' и корзины покупок."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def validate(self, attrs):
        print(attrs)
        user = self.context.get('request').user
        recipes_in_cart = Recipe.objects.filter(is_in_shopping_cart=user)
        recipes_in_favorited = Recipe.objects.filter(is_favorited=user)
        recipe = Recipe.objects.get(id=self.instance.id)
        if recipe in recipes_in_cart:
            raise serializers.ValidationError(
                'Ошибка добавления в список покупок'
            )
        if recipe in recipes_in_favorited:
            raise serializers.ValidationError(
                'Ошибка добавления в избранное'
            )
        return attrs


class SubscriptionUserSerializer(AdvancedUserSerializer):
    """Сериализатор подписки."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count', 'avatar'
        )

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_queryset = Recipe.objects.filter(author=obj)
        recipes_limit = request.query_params.get('recipes_limit')
        try:
            limit = int(recipes_limit)
        except (TypeError, ValueError):
            limit = PAGE_SIZE

        recipes_queryset = recipes_queryset[:limit]
        return ShortRecipeSerializer(
            recipes_queryset, many=True, context=self.context
        ).data
