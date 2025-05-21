from django.urls import path
from .views import SubscriptionListView, SubscriptionCreateDeleteView


urlpatterns = [
    path(
        'subscriptions/',
        SubscriptionListView.as_view(),
        name='subscription-list',
    ),
    path(
        '<int:user_id>/subscribe/',
        SubscriptionCreateDeleteView.as_view(),
        name='subscription-create-delete',
    ),
]
