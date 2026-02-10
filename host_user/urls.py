from django.urls import path

from host_user.views import HostCRUDView, AdminHostListView, AdminHostStatusUpdateView

urlpatterns = [
    path('host/', HostCRUDView.as_view(), name='hostCRUD'),

    # Admin views
    path('admin/hosts/', AdminHostListView.as_view(), name='admin_list_all'),
    path('admin/hosts/<str:status>/', AdminHostListView.as_view(), name='admin_list_status'),
    path('admin/hosts/<int:pk>/update-status/', AdminHostStatusUpdateView.as_view(), name='admin_update_status'),
]