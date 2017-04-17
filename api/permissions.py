from rest_framework import permissions


class IsOwnerOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        """
         Only owner, Admin can read or write or delete
        """
        if(request.user.is_superuser):
            return True
        else:
            return obj.user == request.user