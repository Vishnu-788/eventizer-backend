from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth_user.views import AuthView, CustomTokenObtainPairView

app_name = 'auth_user'
urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', AuthView.as_view(), name='register')
]