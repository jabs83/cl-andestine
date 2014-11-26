from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from coachlogix.base.api.models import ContentBase, ModelBase, TimeStamped
from coachlogix.apps.users.models import Role
from coachlogix.apps.files.models import File
from coachlogix.apps.generic.models import Currency, Location

from . import STATUS_CHOICES


class OrganizationBase(TimeStamped, ContentBase):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=10, blank=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class OrganizationDigest(OrganizationBase):
    """
    An abridged record of an Organization containing only basic information.
    """
    pass

    class Meta:
        verbose_name = _('Organization Digest')
        verbose_name_plural = _('Organization Digests')


class Organization(OrganizationBase):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     through='Membership',
                                     through_fields=('organization', 'user'),
                                     null=True, blank=True)
    connected_organizations = models.ManyToManyField('self', symmetrical=False,
                                                     null=True, blank=True)
    location = models.OneToOneField(Location, null=True, blank=True)
    avatar = models.OneToOneField(File, on_delete=models.SET_NULL,
                                  null=True, blank=True)
    currency = models.ForeignKey(Currency, null=True, blank=True)
    
    def get_members_with_role(self, role):
        """
        Return all members with the :role: passed in as either string or Role object.
        """
        kwargs = {
            'user__pk__in': self.memberships.values_list('user__pk', flat=True),
            'role{}'.format('__name__iexact' if isinstance(role, str) else ''): role,
        }
        return self.memberships.filter(**kwargs)

    def populate_connected_users(self):
        """
        Called when one organization connects to another. This method will add
        the members from the connecting organization to the current one.
        """
        self.memberships.filter(is_employee=False).delete()
        
        # Add all employees of related organization to current one by iterating
        # over all ``Membership`` objects and creating new ones based on those.
        for organization in self.connected_organizations.all():
            for member in organization.memberships.filter(is_employee=True):
                kwargs = {
                    'organization': self,
                    'user': member.user,
                    'role': member.role,
                    'title': member.title,
                    'connected_by': organization,
                    'is_employee': False,
                }
                self.memberships.get_or_create(**kwargs)

    def update_or_create_organization_digest(self):
        """
        Updates or creates a new ``OrganizationDigest`` record based on the
        current organization.
        """
        kwargs = {
            'name': self.name,
            'defaults': {
                'description': self.description,
                'website': self.website,
                'phone': self.phone,
            }
        }
        return OrganizationDigest.objects.update_or_create(**kwargs)


class ProfessionalTitle(ModelBase):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization)

    class Meta:
        verbose_name = _('Professional Title')
        verbose_name_plural = _('Profesional Titles')
        unique_together = ('name', 'organization',)

    def __str__(self):
        return '{} - {}'.format(self.name, self.organization)


class Group(ModelBase):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    organization = models.ForeignKey(Organization,
                                     related_name='organizational_groups')
    children = models.ManyToManyField('self', null=True, blank=True, symmetrical=False)
    
    class Meta:
        unique_together = ('name', 'organization',)

    def __str__(self):
        return self.name


class Membership(TimeStamped, ModelBase):
    organization = models.ForeignKey(Organization,
                                     related_name='memberships')
    groups = models.ManyToManyField(Group, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='memberships')
    role = models.ForeignKey(Role, related_name='organization_memberships')
    title = models.ForeignKey(ProfessionalTitle, null=True, blank=True)
    connected_by = models.ForeignKey(Organization, null=True, blank=True,
                                     editable=False, related_name='connected_members')
    is_employee = models.BooleanField(default=True)
    status = models.PositiveIntegerField(max_length=1, choices=STATUS_CHOICES,
                                         null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.role)

    @classmethod
    def get_for_user(cls, user, organization=None):
        """
        Return a QuerySet of ``Employments`` for given :user: and optional :organization:.
        """
        return cls.objects.filter(user=user)


class Contact(ContentBase):
    organization = models.ForeignKey(Organization, related_name='contacts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.ForeignKey(ProfessionalTitle, null=True, blank=True)

    def __str__(self):
        return '{}{}'.format(self.user, ' -'.join(self.title) if self.title else '')
