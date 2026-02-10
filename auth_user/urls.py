from django.urls import path
from auth_user.views import AuthView, CustomTokenObtainPairView, CookieTokenRefreshView

app_name = 'auth_user'
urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', AuthView.as_view(), name='register')
]