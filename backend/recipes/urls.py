from django.urls import path

from .views import (
    RecipeListCreateView, RecipeRetrieveUpdateDestroyView,
)
from short_links.views import RecipeShortLinkView


urlpatterns = [
    path(
        '',
        RecipeListCreateView.as_view(),
        name='recipe-list-create',
    ),
    path(
        '<int:recipe_id>/',
        RecipeRetrieveUpdateDestroyView.as_view(),
        name='recipe-detail-update-delete',
    ),
    path(
        '<int:recipe_id>/get-link/',
        RecipeShortLinkView.as_view(),
        name='recipe-get-link',
    ),
]
