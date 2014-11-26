from django.db import models
from django.utils.timezone import now

from . import mixins


class ModelBase(models.Model):
    """
    The base model for interfacting with django.db.models.Model.
    """

    class Meta:
        abstract = True
    
    @property
    def _cls(self):
        return self.__class__.__name__.lower()


class ContentBase(mixins.AdminContentMixin,
                  ModelBase):
    """
    The base model for any content related models.
    """

    class Meta:
        abstract = True


class TimeStamped(models.Model):
    created = models.DateTimeField(null=True, editable=False, auto_now_add=True)
    updated = models.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        _now = now()
        self.updated = _now
        super(TimeStamped, self).save(*args, **kwargs)
