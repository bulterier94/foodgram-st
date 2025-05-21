from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserRegisterSerializer, UserDetailSerializer, UserAvatarSerializer,
    UserSetPasswordSerializer,
)
from .models import User


class UserViewMixin:
    queryset = User.objects.all()


class UserListView(UserViewMixin, generics.ListAPIView,):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserDetailSerializer
        return UserRegisterSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'email': user.email,
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(UserViewMixin, generics.RetrieveAPIView,):

    serializer_class = UserDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'


class UserSelfDetailView(UserViewMixin, generics.RetrieveAPIView,):

    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user


class UserAvatarUpdateDeleteView(
    UserViewMixin, generics.UpdateAPIView, generics.DestroyAPIView,
):

    serializer_class = UserAvatarSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()

        if user.avatar:
            storage = user.avatar.storage
            path = user.avatar.path
            storage.delete(path)

            user.avatar.delete(save=False)
            user.avatar = None
            user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSetPasswordView(
    UserViewMixin, generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
