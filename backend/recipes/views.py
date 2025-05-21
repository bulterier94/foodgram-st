from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import Recipe, IngredientInRecipe
from .serializers import (
    RecipeReadSerializer, RecipeCreateSerializer, RecipeUpdateSerializer
)
from core.permissions import IsAuthorOrReadOnly


class RecipeMixin:
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class RecipeListCreateView(RecipeMixin, generics.ListCreateAPIView):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateSerializer
        return RecipeReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        recipe = Recipe.objects.create(
            author=request.user,
            name=serializer.validated_data['name'],
            text=serializer.validated_data['text'],
            cooking_time=serializer.validated_data['cooking_time'],
            image=serializer.validated_data.get('image')
        )

        ingredients = [
            IngredientInRecipe(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount']
            )
            for ingredient in serializer.validated_data['ingredients']
        ]
        IngredientInRecipe.objects.bulk_create(ingredients)

        output_serializer = RecipeReadSerializer(
            recipe, context=self.get_serializer_context()
        )
        return Response(output_serializer.data, status=status.HTTP_201_CREATED,)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if author_id := self.request.query_params.get('author'):
            queryset = queryset.filter(author_id=author_id)

        if is_favorited := self.request.query_params.get('is_favorited'):
            if user.is_authenticated:
                filter_q = Q(favorite_recipe__user=user)
                queryset = queryset.filter(
                    filter_q if is_favorited == '1' else ~filter_q
                )

        if is_in_cart := self.request.query_params.get('is_in_shopping_cart'):
            if user.is_authenticated:
                filter_q = Q(shopping_cart_recipe__user=user)
                queryset = queryset.filter(
                    filter_q if is_in_cart == '1' else ~filter_q
                )

        return queryset


class RecipeRetrieveUpdateDestroyView(
    RecipeMixin, generics.RetrieveUpdateDestroyAPIView
):
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'recipe_id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return RecipeUpdateSerializer
        return RecipeReadSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        for attr, value in serializer.validated_data.items():
            if attr != 'ingredients':
                setattr(instance, attr, value)
        instance.save()

        if 'ingredients' in serializer.validated_data:
            instance.recipe_from_ingredient.all().delete()
            ingredients = [
                IngredientInRecipe(
                    recipe=instance,
                    ingredient_id=ingredient['id'],
                    amount=ingredient['amount']
                )
                for ingredient in serializer.validated_data['ingredients']
            ]
            IngredientInRecipe.objects.bulk_create(ingredients)

        output_serializer = RecipeReadSerializer(
            instance, context=self.get_serializer_context()
        )
        return Response(output_serializer.data,)
