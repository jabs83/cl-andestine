from django.db import models

from coachlogix.base.api.models import ModelBase


class Currency(ModelBase):
    pass


class Location(ModelBase):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
