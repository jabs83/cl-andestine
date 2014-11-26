from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from coachlogix.base.api.models import ContentBase, ModelBase, TimeStamped


class Plan(ModelBase):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # cost = models.ForeignKey(PlanCost, null=True, blank=True)


class Subscription(ModelBase):
    plan = models.OneToOneField(Plan)
    status = models.PositiveIntegerField(max_length=1, null=True, blank=True)
    payment_method = models.PositiveIntegerField(null=True, blank=True)


class Account(TimeStamped, ContentBase):
    plan = models.ForeignKey(Plan, null=True, blank=True)
    subscription = models.ForeignKey(Subscription, null=True, blank=True)

    @property
    def type(self):
        return self._cls.rstrip('account')
    
    @property
    def name(self):
        return self.owner.primary_email

    @property
    def owner(self):
        return self.user if hasattr(self, 'user') else self.organization


class UserAccount(Account):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                related_name='account')
   
    class Meta:
        verbose_name = _('User Account')
        verbose_name_plural = _('User Accounts')


class OrganizationAccount(Account):
    organization = models.OneToOneField('organizations.Organization',
                                        related_name='account')
    
    class Meta:
        verbose_name = _('Organization Account')
        verbose_name_plural = _('Organization Accounts')
