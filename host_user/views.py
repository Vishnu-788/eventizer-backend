from django.db.models import QuerySet
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    get_object_or_404,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from auth_user.permissions import IsHost, IsCustomAdmin, IsVerifiedHost

from .serializers import (
    HostCreateSerializer,
    HostStatusUpdateSerializer,
    HostSerializer,
)
from .models import Host


"""
View for User.Role == 'Host'.
Host must have a entry in the user table.
"""


class HostCreateView(CreateAPIView):
    permission_classes = [IsHost]
    serializer_class = HostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HostDetailUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsVerifiedHost]
    serializer_class = HostSerializer

    def get_object(self):
        return Host.objects.get(user=self.request.user)


class HostNotVerifiedView(RetrieveAPIView):
    permission_classes = [IsHost]
    serializer_class = HostSerializer

    def get_object(self):
        try:
            host = Host.objects.get(user=self.request.user)
        except Host.DoesNotExist:
            raise NotFound(detail={"code": "verification_not_started"})
        return host


"""
Custom Admin view.
Returns all the hosts regardless of the status field.
If query params == 'approved': returns all the hosts with status field marked as 'approved'.
If query params == 'rejected': returns all the hosts with status field marked as 'rejected'.
"""


class AdminHostListView(ListAPIView):
    permission_classes = [IsCustomAdmin]
    serializer_class = HostSerializer

    def get_queryset(self) -> QuerySet:
        status_param = self.request.query_params.get("status")
        if status_param:
            query_set = Host.objects.filter(status=status_param)
        else:
            query_set = Host.objects.all()
        return query_set


class AdminHostStatusUpdateView(UpdateAPIView):
    permission_classes = [IsCustomAdmin]
    queryset = Host.objects.all()
    serializer_class = HostStatusUpdateSerializer
    lookup_field = "pk"
