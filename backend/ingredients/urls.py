from django.urls import path

from .views import IngredientListView, IngredientDetailView


urlpatterns = [
    path(
        '',
        IngredientListView.as_view(),
        name='ingredient-list',
    ),
    path(
        '<int:ingredient_id>/',
        IngredientDetailView.as_view(),
        name='ingredient-detail',
    ),
]
