from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from applications.users.views_api import UsuarioListAPIView, UsuarioDetailAPIView, UserMeAPIView, RegisterAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('applications.home.urls')),
    path('users/', include('applications.users.urls')),

    # API JWT
    path('api/token/', TokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='api-token-verify'),
    path('api/register/', RegisterAPIView.as_view(), name='api-register'),
    path('api/usuarios/me/', UserMeAPIView.as_view(), name='api-user-me'),
    path('api/usuarios/', UsuarioListAPIView.as_view(), name='api-user-list'),
    path('api/usuarios/<int:pk>/', UsuarioDetailAPIView.as_view(), name='api-user-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)