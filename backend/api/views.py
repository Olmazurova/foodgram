from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AdvancedUserSerializer

User = get_user_model()


class AvatarView(APIView):
    """Представление для добавления и удаления аватара пользователя."""

    def put(self, request):
        user = request.user
        serializer = AdvancedUserSerializer(
            user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        user = request.user
        user.avatar = None
        user.save(update_fields=['avatar'])
        return Response(
            {'message': 'Аватар успешно удалён'},
            status=status.HTTP_204_NO_CONTENT
        )
