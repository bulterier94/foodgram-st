from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .serializers import UserSubscriptionSerializer, SubscriptionSerializer
from .models import Subscription
from users.models import User


class SubscriptionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSubscriptionSerializer

    def get_queryset(self):
        return User.objects.filter(
            subscribed_on__subscriber=self.request.user,
        )


class SubscriptionCreateDeleteView(
    generics.CreateAPIView, generics.DestroyAPIView
):

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated,]

    def create(self, request, *args, **kwargs):
        subscribed_on_id = kwargs.get('user_id')
        subscribed_on_user = get_object_or_404(
            User, id=subscribed_on_id,
        )

        if request.user == subscribed_on_user:
            return Response(
                {'detail': 'Нельзя подписаться на самого себя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subscription, created = Subscription.objects.get_or_create(
            subscriber=request.user,
            subscribed_on=subscribed_on_user,
        )

        if not created:
            return Response(
                {'detail': 'Вы уже подписаны на этого пользователя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserSubscriptionSerializer(
            subscription.subscribed_on,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        subscribed_on_id = kwargs.get('user_id')
        subscribed_on_user = get_object_or_404(
            User, id=subscribed_on_id,
        )

        deleted, _ = Subscription.objects.filter(
            subscriber=request.user,
            subscribed_on=subscribed_on_user,
        ).delete()

        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'detail': 'Вы не подписаны на этого пользователя.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
