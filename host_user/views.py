from urllib.request import Request

from django.db.models import QuerySet
from rest_framework.generics import GenericAPIView, get_object_or_404, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from auth_user.permissions import IsHost, IsCustomAdmin

from .serializers import HostCRUDSerializer, HostListSerializer, HostStatusUpdateSerializer
from .models import Host


"""
This view is for user with role 'host'. They can update the other fields except the status field which can updated
only via 'admin' user.
"""
class HostCRUDView(GenericAPIView):
    permission_classes = [IsHost]
    serializer_class = HostCRUDSerializer

    def get_object(self) -> Host:
        return get_object_or_404(Host, user=self.request.user)

    def get(self, request: Request) -> Response:
        host = self.get_object()
        serializer = self.get_serializer(host)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user = self.request.user)
        return Response(
            {"success": "Successfully created."},
            status=status.HTTP_201_CREATED
        )

    def patch(self):
        pass

    def delete(self):
        pass

"""
Custom Admin view.
Returns all the hosts regardless of the status field.
If query params == 'approved': returns all the hosts with status field marked as 'approved'.
If query params == 'rejected': returns all the hosts with status field marked as 'rejected'.
"""
class AdminHostListView(ListAPIView):
    permission_classes = [IsCustomAdmin]
    serializer_class = HostListSerializer
    def get_queryset(self) -> QuerySet:
        status_param = self.request.query_params.get("status")
        if status_param:
            query_set = Host.objects.filter(status=status_param)
        else:
            query_set = Host.objects.all()
        print(query_set)
        return query_set

class AdminHostStatusUpdateView(UpdateAPIView):
    permission_classes = [IsCustomAdmin]
    queryset = Host.objects.all()
    serializer_class = HostStatusUpdateSerializer
    lookup_field = 'pk'

