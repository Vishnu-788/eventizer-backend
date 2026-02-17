from django.urls import path

from host_user.views import HostCRUDView, AdminHostListView, AdminHostStatusUpdateView, HostDetailView

urlpatterns = [
    path('host/', HostCRUDView.as_view(), name='hostCRUD'),
    path('host/<str:username>/', HostDetailView.as_view(), name='host-detail'),

    # Admin views
    path('admin/hosts/', AdminHostListView.as_view(), name='admin_list_all'),
    path('admin/hosts/<str:status>/', AdminHostListView.as_view(), name='admin_list_status'),
    path('admin/hosts/<int:pk>/update-status/', AdminHostStatusUpdateView.as_view(), name='admin_update_status'),
]