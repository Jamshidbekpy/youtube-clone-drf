from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = "Only the owner can perform this action."

    def has_object_permission(self, request, view, obj):
        return obj.channel == request.user.channel
class IsOwner2(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user.channel
   
class HasChannel(BasePermission):
    def has_permission(self, request, view):
        return bool(hasattr(request.user, "channel") and request.user.channel)