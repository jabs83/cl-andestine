from rest_framework import viewsets

from . import serializers
from . import models


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrganizationSerializer
    queryset = models.Organization.objects.all()
