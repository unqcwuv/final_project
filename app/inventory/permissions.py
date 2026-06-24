from rest_framework.permissions import BasePermission

class IsStorageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_company_owner
                and obj.company_id == request.user.company_id)

class IsCompanyMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company_id == request.user.company_id