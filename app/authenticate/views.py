from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Company
from .serializers import (
    RegisterSerializer, CompanySerializer,
    AddEmployeeSerializer, EmployeeSerializer)
from .permissions import IsCompanyOwner, IsCompanyOwnerUser

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class CompanyCreateView(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [permissions.IsAuthenticated(), IsCompanyOwner()]
        return [permissions.IsAuthenticated()]

class AddEmployeeView(generics.GenericAPIView):
    serializer_class = AddEmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyOwnerUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save(company=request.user.owned_company)
        return Response(
            {'detail': f'Пользователь {employee.email} добавлен в компанию'},
            status=status.HTTP_200_OK,
        )

class EmployeeListView(generics.ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyOwnerUser]

    def get_queryset(self):
        return self.request.user.owned_company.employees.filter(is_company_owner=False)

class RemoveEmployeeView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCompanyOwnerUser]
    lookup_url_kwarg = 'employee_id'

    def get_queryset(self):
        return self.request.user.owned_company.employees.all()

    def perform_destroy(self, instance):
        instance.company = None
        instance.save(update_fields=['company'])
