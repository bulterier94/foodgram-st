from rest_framework.views import exception_handler
from django.http import Http404
from rest_framework_simplejwt.exceptions import InvalidToken


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, Http404):
        response.data = {
            'detail': 'Страница не найдена.',
        }

    if isinstance(exc, InvalidToken):

        response.data = {
            "error": {
                "code": "invalid_token",
                "message": "Токен недействителен.",
                "detail": {
                    "reason":
                        'Время жизни токена истекло или он в чёрном списке.',
                    "action": "Пожалуйста, выполните вход заново."
                }
            }
        }

    return response
