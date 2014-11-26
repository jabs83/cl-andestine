from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import ugettext_lazy as _

from coachlogix.base.api.models import ModelBase, TimeStamped
from coachlogix.apps.organizations.models import Organization
from coachlogix.apps.users.models import Role

from . import STATUS_CHOICES


class Roadmap(ModelBase):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
   
    def __str__(self):
        return self.name

    @property
    def item_count(self):
        return self.items.count()

    @property
    def is_complete(self):
        pass


class RoadmapItem(TimeStamped, ModelBase):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    roadmap = models.ForeignKey(Roadmap, related_name='items')

    ITEM_CHOICES = models.Q(app_label='files', model='file')
    item_type = models.ForeignKey(ContentType, limit_choices_to=ITEM_CHOICES,
                                  null=True, blank=True)
    item_id = models.PositiveIntegerField(null=True, blank=True)
    item = GenericForeignKey('item_type', 'item_id')
    estimated_start = models.DateField(null=True, blank=True)
    estimated_finish = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check and set the order field if it is empty.
        if not self.order:
            try:
                klass = self.__class__
                last = klass._default_manager.all().order_by('-order').first()
                self.order = last.order + 1
            except Exception:
                self.order = 0
        super().save(*args, **kwargs)


class Engagement(TimeStamped, ModelBase):
    emperor = models.ForeignKey('accounts.Account', related_name='engagements',
                                null=True, blank=True)
    proctor = models.ForeignKey('accounts.Account', related_name='engagements_proctered',
                                null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     through='Membership',
                                     through_fields=('engagement', 'user'),
                                     related_name='engagements')
    roadmap = models.OneToOneField(Roadmap, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.PositiveIntegerField(max_length=1, choices=STATUS_CHOICES, blank=True)

    def __str__(self):
        return 'Created {} - {} Members'.format(self.created.strftime('%b %d, %Y'),
                                                self.members.count())

    def get_members_with_role(self, role):
        """
        Return all members with the :role: passed in as either string or Role object.
        """
        kwargs = {
            'user__pk__in': self.members.values_list('users__pk', flat=True),
            'role{}'.format('__name__iexact' if isinstance(role, str) else ''): role,
        }
        return Membership.objects.filter(**kwargs)

    @property
    def is_activated(self):
        pass

    @property
    def duration(self):
        pass


class Membership(ModelBase):
    engagement = models.ForeignKey(Engagement)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    role = models.ForeignKey(Role)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True, blank=True,
                                   related_name='membership_invites')

    def __str__(self):
        return '{} - {}'.format(self.user, self.role)

class Goal(ModelBase):
    pass
