from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    "Only the owner can perform this action."
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user