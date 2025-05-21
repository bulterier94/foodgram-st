from rest_framework import serializers

from users.models import User
from users.serializers import UserDetailSerializer
from .models import Subscription
from core.serializers import Base64ImageField
from recipes.models import Recipe


class UserRecipeSerializer(serializers.ModelSerializer):

    image = Base64ImageField(read_only=True,)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]


class UserSubscriptionSerializer(UserDetailSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
            'recipes',
            'recipes_count',
        ]

    def get_is_subscribed(self, obj):
        return True

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get(
            'recipes_limit'
        ) if request else None

        queryset = obj.recipe_author.all()

        if recipes_limit:
            try:
                recipes_limit = int(recipes_limit)
                queryset = queryset[:recipes_limit]
            except ValueError:
                pass

        serializer = UserRecipeSerializer(
            queryset, many=True, context=self.context,
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipe_author.count()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['subscriber', 'subscribed_on',]
