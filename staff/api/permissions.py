from rest_framework import permissions


class IsTopManegment(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=('Top Management',)).exists()
