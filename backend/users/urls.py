from django.urls import path
from .views import (
    UserListView, UserDetailView, UserSelfDetailView,
    UserAvatarUpdateDeleteView, UserSetPasswordView,
)


urlpatterns = [
    path(
        '',
        UserListView.as_view(),
        name='user-list',
    ),
    path(
        '<int:user_id>/',
        UserDetailView.as_view(),
        name='user-detail',
    ),
    path(
        'me/',
        UserSelfDetailView.as_view(),
        name='user-self-detail',
    ),
    path(
        'me/avatar/',
        UserAvatarUpdateDeleteView.as_view(),
        name='user-self-avatar-update-delete',
    ),
    path(
        'set_password/',
        UserSetPasswordView.as_view(),
        name='user-set-password',
    ),
]
