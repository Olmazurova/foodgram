from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView


class GetUserMixin:
    """Добавляет метод get_user, возвращающий user из request."""

    def get_user(self):
        return self.request.user


class AuthenticatedPermissionMixin(GetUserMixin, APIView):
    """Добавляет класс разрешений IsAuthenticated."""

    permission_classes = [IsAuthenticated,]


class AllowAnyPermissionsMixin(APIView):
    """Добавляет класс разрешений AllowAny."""

    permission_classes = [AllowAny,]


class NonePaginationPermissionMixin(AllowAnyPermissionsMixin):
    """Убирает пагинацию."""

    pagination_class = None
