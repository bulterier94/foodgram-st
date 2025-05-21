from rest_framework import generics
from django.db.models import Q

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientListView(generics.ListAPIView):

    pagination_class = None
    serializer_class = IngredientSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('name', None)

        if not search_query:
            return Ingredient.objects.all()

        queryset = Ingredient.objects.filter(
            Q(name__istartswith=search_query),
        )

        return queryset


class IngredientDetailView(generics.RetrieveAPIView):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'ingredient_id'
