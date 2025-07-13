from django.urls import include, path

from .views import AvatarView

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/me/avatar/', AvatarView.as_view(), name='avatar'),
]