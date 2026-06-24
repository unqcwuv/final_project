from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Storage
from .serializers import StorageSerializer
from .permissions import IsStorageOwner, IsCompanyMember

class StorageCreateView(generics.CreateAPIView):
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_company_owner:
            raise PermissionDenied('Только владелец компании может создать склад')
        serializer.save()

class StorageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), IsCompanyMember()]
        return [permissions.IsAuthenticated(), IsStorageOwner()]

