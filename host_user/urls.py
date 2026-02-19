from django.urls import path

from host_user.views import AdminHostListView, AdminHostStatusUpdateView, HostCreateView, HostDetailUpdateView, \
    HostNotVerifiedView

urlpatterns = [
    path('me/', HostDetailUpdateView.as_view(), name='host_detail_update'),
    path('me/not-verified/', HostNotVerifiedView.as_view(), name='host_not_verified'),
    path('create/', HostCreateView.as_view(), name='create_host'),

    # Admin views
    path('admin/', AdminHostListView.as_view(), name='admin_list_all'),
    path('admin/<str:status>/', AdminHostListView.as_view(), name='admin_list_status'),
    path('admin/<int:pk>/update-status/', AdminHostStatusUpdateView.as_view(), name='admin_update_status'),
]