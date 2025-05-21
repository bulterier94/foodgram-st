from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken, OutstandingToken,
)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate


class LoginAPIView(generics.GenericAPIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            token = AccessToken.for_user(user)
            return Response({
                'auth_token': str(token),
            })
        return Response({'detail': 'Неверный email или пароль.'}, status=400)


class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        try:
            token_str = str(request.auth)
            access_token = AccessToken(token=token_str)
            outstanding_token, created = OutstandingToken.objects.get_or_create(
                token=token_str,
                defaults={
                    'user': request.user,
                    'jti': access_token['jti'],
                    'expires_at': datetime.fromtimestamp(access_token['exp']),
                }
            )

            BlacklistedToken.objects.get_or_create(token=outstanding_token)

            return Response(status=status.HTTP_204_NO_CONTENT)

        except TokenError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
