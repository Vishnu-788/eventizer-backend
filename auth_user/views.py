
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .serailizers import UserSerializer, CustomTokenObtainPairSerializer, UserRetrieveUpdateSerializer
from .models import User
"""
For registering the user.
"""
class AuthView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "id": user.id,
            "username": user.username,
            "role": user.role
        }, status=status.HTTP_201_CREATED)


"""
Overriding the 'ObtainPairView' to modify the data from response body.
returns -> username, access token, refresh token(Http cookie only), role, verified.
"""
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        response: Response = super().post(request, *args, **kwargs)
        refresh = response.data['refresh']
        if refresh:
            response.set_cookie(
                key='refresh',
                value=refresh,
                httponly=True,
                max_age=60 * 60 * 24 * 7,
                secure=False,
                samesite='Lax'
            )
            del response.data['refresh']
        return response


"""
Without Overriding the TokenRefreshView, Django is not looking for the refresh token on the request cookie.
"""
class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh")
        serializer = self.get_serializer(data={"refresh": refresh})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class UserRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserRetrieveUpdateSerializer

    def get_object(self) -> User:
        return self.request.user


class LogoutView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        response = Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
        response.delete_cookie("refresh")
        return response





