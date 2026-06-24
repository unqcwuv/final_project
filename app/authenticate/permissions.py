from rest_framework.permissions import BasePermission

class IsCompanyOwnerUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_company_owner
        )

class IsCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
