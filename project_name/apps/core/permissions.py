from enum import Enum
from functools import wraps
from typing import Any
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import BasePermission

User = get_user_model()


class PermissionEnum(Enum):
    """Permissions Enum. Always adds permissions, does not delete permission."""

    @classmethod
    def get_permissions(cls):
        return [(perm.name, perm.value) for perm in cls]

    @classmethod
    def get_app_label(cls):
        raise NotImplementedError()

    @property
    def perm(self):
        return f"{self.get_app_label()}.{self.name}"


def require_permission(
    permissions: list[PermissionEnum] | PermissionEnum, has_ref: bool = True
) -> Any:
    if not isinstance(permissions, list):
        permissions = [permissions]

    required_permissions = [
        p.perm for p in permissions if isinstance(p, PermissionEnum)
    ]
    if len(required_permissions) != len(permissions):
        raise Exception("All permissions should be derived from PermissionEnum")

    def permission_decorator(endpoint):
        @wraps(endpoint)
        def wrapper(*args, **kwargs):
            request = args[1] if has_ref else args[0]

            user = request.user
            if not isinstance(user, User):
                return Response(status=status.HTTP_400_BAD_REQUEST)

            allowed = user.has_perms(required_permissions)
            if not allowed:
                return Response("Access Denied", status=status.HTTP_403_FORBIDDEN)

            return endpoint(*args, **kwargs)

        return wrapper

    return permission_decorator


# https://stackoverflow.com/questions/19313314/django-rest-framework-viewset-per-action-permissions
class TruboardPermissions(BasePermission):
    permissions = {
        # "action-name": list[permission enum]
    }

    def has_permission(self, request, view):
        is_authenticated = bool(request.user and request.user.is_authenticated)
        if not is_authenticated:
            return False

        action_permissions = self.permissions.get(view.action, None)
        if action_permissions is None:
            return False

        required_permissions = [
            p.perm if isinstance(p, PermissionEnum) else p for p in action_permissions
        ]

        return request.user.has_perms(required_permissions)
