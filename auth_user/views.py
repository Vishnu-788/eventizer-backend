
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth_user.serailizers import UserSerializer


# Create your views here.
class AuthView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer = UserSerializer

    def post(self, request):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "id": user.id,
            "username": user.username,
            "role": user.role
        }, status=status.HTTP_201_CREATED)





