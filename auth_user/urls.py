from django.urls import path
from auth_user.views import AuthView

app_name = 'users'
urlpatterns = [
    path('register/', AuthView.as_view(), name='register')
]