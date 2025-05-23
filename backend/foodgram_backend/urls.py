from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', include('authentication.urls')),
    path('api/users/', include('users.urls')),
    path('api/users/', include('subscriptions.urls')),
    path('api/ingredients/', include('ingredients.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/recipes/', include('favorite_recipes.urls')),
    path('api/recipes/', include('shopping_cart.urls')),
    path('', include('short_links.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
