from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            user_and_token = super().authenticate(request)
            if user_and_token is None:
                return None

            user, token = user_and_token

            jti = token['jti']
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise InvalidToken('Токен в черном списке.')

            return (user, token)

        except Exception as e:
            raise InvalidToken(str(e))
