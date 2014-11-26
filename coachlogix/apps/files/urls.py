from django.conf.urls import patterns, url

from rest_framework import routers

from . import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'files', views.FileViewSet)

urlpatterns = router.urls
