from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class BookPermission(BasePermission):
    """
    Custom permission class to authenticate user permission.
    """

    def has_permission(self, request, view):
        scope = {
            "GET": "view",
            "POST": "add",
            "PUT": "change",
            "PATCH": "change",
            "DELETE": "delete",
        }
        available_permissions = Permission.objects.get(content_type=ContentType.objects.get(model=view.basename),
                                                       codename__contains=scope[request.method])

        if request.user.has_perm(
                available_permissions.codename) or f'{available_permissions.content_type.app_label}.{available_permissions.codename}' in request.user.get_group_permissions():
            return True
        raise PermissionDenied()
