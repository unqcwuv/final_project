from django.urls import path

from .views import RegisterView, CompanyCreateView, CompanyDetailView, EmployeeListView, AddEmployeeView, \
    RemoveEmployeeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('companies/', CompanyCreateView.as_view(), name='company-create'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('companies/employees/', EmployeeListView.as_view(), name='employee-list'),
    path('companies/employees/add/', AddEmployeeView.as_view(), name='employee-add'),
    path('companies/employees/<int:employee_id>/', RemoveEmployeeView.as_view(), name='employee-remove'),
]