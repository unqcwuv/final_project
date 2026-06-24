from django.urls import path
from .views import StorageCreateView, StorageDetailView

urlpatterns = [
    path('storages/', StorageCreateView.as_view(), name='storage-create'),
    path('storages/<int:pk>/', StorageDetailView.as_view(), name='storage-detail'),
]