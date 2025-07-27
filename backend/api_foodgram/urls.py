from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

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
    path(
        'api/about/',
        TemplateView.as_view(
            template_name='frontend/src/pages/about/index.js'
        ),
        name='about'
    ),
    path(
        'api/technologies/',
        TemplateView.as_view(
            template_name='frontend/src/pages/technologies/index.js'
        ),
        name='technologies'
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
