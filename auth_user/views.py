
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from auth_user.serailizers import UserSerializer, CustomTokenObtainPairSerializer

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
                secure=False,
                samesite='Lax'
            )
            del response.data['refresh']
        return response




