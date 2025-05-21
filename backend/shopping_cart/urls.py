from django.urls import path

from .views import (
    ShoppingCartCreateDeleteView, ShoppingCartDownloadPDF,
)


urlpatterns = [
    path(
        '<int:recipe_id>/shopping_cart/',
        ShoppingCartCreateDeleteView.as_view(),
        name='shopping-cart-create-delete',
    ),
    path(
        'download_shopping_cart/',
        ShoppingCartDownloadPDF.as_view(),
        name='shopping-cart-download',
    ),
]
