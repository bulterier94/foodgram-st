from rest_framework import serializers

from .models import RecipeShortLink


class RecipeShortLinkSerializer(serializers.ModelSerializer):
    short_link = serializers.SerializerMethodField()

    class Meta:
        model = RecipeShortLink
        fields = ['short_link',]

    def get_short_link(self, obj):
        request = self.context.get('request')
        return obj.get_short_url(request)
