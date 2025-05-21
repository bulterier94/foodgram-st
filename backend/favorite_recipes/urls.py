from django.urls import path

from .views import FavoriteRecipeCreateDeleteView


urlpatterns = [
    path(
        '<int:recipe_id>/favorite/',
        FavoriteRecipeCreateDeleteView.as_view(),
        name='favorite-recipe-create-delete',
    ),
]
