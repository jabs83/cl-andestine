from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic.base import TemplateView

from .routers import router

urlpatterns = [
    # API
    url(r'^api/v1/', include(router.urls)),

    # Authentication
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),

    # Admin site.
    url(r'^admin/', include(admin.site.urls)),

    # Load App
    url(r'^$', TemplateView.as_view(template_name='main_app.html'), name='main-app-view'),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
