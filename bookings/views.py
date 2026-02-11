from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


# Create your views here.
class BookingsView(GenericAPIView):
    def post(self, request: Request) -> Response:
        pass
