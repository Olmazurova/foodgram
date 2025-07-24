from django.contrib import admin

from .models import User

admin.site.empty_value_display = 'Не задано'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Администрирование пользователей."""

    list_display = (
        'first_name', 'last_name', 'username', 'email', 'password', 'avatar'
    )
    search_fields = ('email', 'first_name')
    list_display_links = ('first_name', 'last_name', 'username', 'email')
