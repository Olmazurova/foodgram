from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from api.constants import PREFIX
from api.views import DecodeLinkView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    re_path(
        rf'{PREFIX}/(?P<hex_id>(0x)?[0-9a-f]+)/',
        DecodeLinkView.as_view(),
        name='decode_link'
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
