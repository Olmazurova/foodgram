from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrAdminOrReadOnly(BasePermission):
    """
    Разрешения: анонимы могут смотреть всё, а CRUD:
    создавать - авторизованные пользователи,
    редактировать/удалять - авторы, админы и суперюзеры.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_staff
            or request.user.is_superuser
        )

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user and request.user.is_authenticated)
        )


class IsAuthenticatedOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return ((request.method in SAFE_METHODS
                and request.user and request.user.is_authenticated)
                or request.user.is_staff
                or request.user.is_superuser)
