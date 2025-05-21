from rest_framework import status, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect

from recipes.models import Recipe
from .models import RecipeShortLink
from .serializers import RecipeShortLinkSerializer


class RecipeShortLinkView(generics.RetrieveAPIView):

    queryset = Recipe.objects.all()
    serializer_class = RecipeShortLinkSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'recipe_id'

    def retrieve(self, request, *args, **kwargs):
        recipe = self.get_object()

        short_link, created = RecipeShortLink.objects.get_or_create(
            recipe=recipe
        )

        serializer = RecipeShortLinkSerializer(
            short_link, context={'request': request}
        )

        return Response(
            {
                'short-link': serializer.data['short_link'],
            },
            status=status.HTTP_200_OK,
        )


def redirect_short_link(request, code):
    short_link = get_object_or_404(RecipeShortLink, code=code)

    short_link.clicks += 1
    short_link.save()

    return redirect(
        short_link.get_absolute_url(request=request)
    )
