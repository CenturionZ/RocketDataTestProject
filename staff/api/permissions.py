from rest_framework import permissions


class IsTopManagement(permissions.BasePermission):
    """
    Наличие у пользователя определенной группы прав (права просмотра сотрудников staff.view)
    """
    def has_permission(self, request, view):
        """
        Проверяет наличие пользователя в списке ему подобных группы Top Management
        :return: bool
        """
        return request.user.groups.filter(name__in=('Top Management',)).exists()
