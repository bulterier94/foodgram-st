from rest_framework import serializers
from .models import ShoppingCart


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='recipe.id', read_only=True,
    )
    name = serializers.CharField(
        source='recipe.name', read_only=True,
    )
    image = serializers.ImageField(
        source='recipe.image', read_only=True,
    )
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time', read_only=True,
    )

    class Meta:
        model = ShoppingCart
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]


class ShoppingCartDownloadSerializer(ShoppingCartSerializer):
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
            'ingredients',
        ]

    def get_ingredients(self, obj):
        return [
            {
                'name': ingredient_rel.ingredient.name,
                'amount': ingredient_rel.amount,
                'measurement_unit': ingredient_rel.ingredient.measurement_unit
            }
            for ingredient_rel in obj.recipe.recipe_from_ingredient.all()
        ]
