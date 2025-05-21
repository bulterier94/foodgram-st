from rest_framework import serializers

from .models import Recipe, IngredientInRecipe
from shopping_cart.models import ShoppingCart
from favorite_recipes.models import FavoriteRecipe
from users.serializers import UserDetailSerializer
from core.serializers import Base64ImageField
from ingredients.models import Ingredient


class IngredientInRecipeReadSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id',)
    name = serializers.ReadOnlyField(source='ingredient.name',)
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = IngredientInRecipe
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount',
        ]


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserDetailSerializer(read_only=True,)
    ingredients = IngredientInRecipeReadSerializer(
        many=True,
        source='recipe_from_ingredient',
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return FavoriteRecipe.objects.filter(
                user=user,
                recipe=obj,
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=user,
                recipe=obj,
            ).exists()
        return False


class IngredientInRecipeWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = IngredientInRecipe
        fields = ['id', 'amount']


class RecipeWriteBaseSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=False,)
    ingredients = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
    )

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'text',
            'cooking_time',
            'image',
            'ingredients',
        ]

    def validate_ingredients(self, value):
        exceptions = []

        if not value:
            exceptions.append('Добавьте хотя бы 1 ингредиент.')

        ingredient_ids = [ingredient['id'] for ingredient in value]
        existing_ids = set(Ingredient.objects.filter(
            id__in=ingredient_ids
        ).values_list('id', flat=True))

        non_existent_ingredients = [
            str(i) for i in ingredient_ids if i not in existing_ids
        ]

        if non_existent_ingredients:
            if len(non_existent_ingredients) == 1:
                exceptions.append(
                    f'Несуществующий ингредиент с id: {non_existent_ingredients[0]}.'
                )
            else:
                exceptions.append(
                    f'Несуществующие ингредиенты с id: {', '.join(non_existent_ingredients)}.'
                )

        try:
            if any(ingredient['amount'] < 1 for ingredient in value):
                exceptions.append(
                    'Количество ингредиента должно быть больше 1.'
                )
        except Exception:
            exceptions.append(
                'Количество ингредиента передано в некорректном формате.'
            )

        unique_ids = set(ingredient['id'] for ingredient in value)
        if len(unique_ids) != len(value):
            exceptions.append('Ингредиенты не должны дублироваться.')

        if exceptions:
            raise serializers.ValidationError(exceptions)

        return value


class RecipeCreateSerializer(RecipeWriteBaseSerializer):
    image = Base64ImageField(required=True, allow_null=False,)


class RecipeUpdateSerializer(RecipeWriteBaseSerializer):
    image = Base64ImageField(required=False, allow_null=False,)
