from rest_framework import serializers
from .models import FavoriteRecipe


class FavoriteRecipeSerializer(serializers.ModelSerializer):
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
        model = FavoriteRecipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]
