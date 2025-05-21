from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import FavoriteRecipe
from recipes.models import Recipe
from .serializers import (
    FavoriteRecipeSerializer,
)


class FavoriteRecipeCreateDeleteView(
    generics.CreateAPIView, generics.DestroyAPIView,
):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = FavoriteRecipeSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'recipe_id'

    def get_object(self):
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)

        try:
            return FavoriteRecipe.objects.get(
                user=self.request.user, recipe=recipe,
            )
        except FavoriteRecipe.DoesNotExist:
            raise ValidationError(
                {"detail": "Рецепт не найден в вашем избранном."},
                code=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if FavoriteRecipe.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            return Response(
                {"detail": "Рецепт уже в избранном."},
                status=status.HTTP_400_BAD_REQUEST
            )

        favorite = FavoriteRecipe.objects.create(
            user=request.user, recipe=recipe
        )
        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
