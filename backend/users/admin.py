from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import User

# В интерфейс админ-зоны нужно вывести необходимые поля моделей и настроить поиск:
# вывести все модели с возможностью редактирования и удаления записей;
# для модели пользователей добавить поиск по адресу электронной почты и имени пользователя;

admin.site.empty_value_display = 'Не задано'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Администрирование пользователей."""

    list_display = (
        'first_name', 'last_name', 'username', 'email', 'password', 'avatar'
    )
    search_fields = ('email', 'first_name')
    list_display_links = ('first_name', 'last_name', 'username', 'email')
