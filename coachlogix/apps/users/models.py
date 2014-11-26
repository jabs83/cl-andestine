from django.db import models
from django.conf import settings
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from coachlogix.base.api.models import ContentBase, ModelBase, TimeStamped
from coachlogix.apps.accounts.models import UserAccount

from . import managers


class User(TimeStamped, PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    first_name = models.CharField(_('first name'), max_length=128, blank=True)
    middle_name = models.CharField(_('first name'), max_length=128, blank=True)
    last_name = models.CharField(_('last name'), max_length=128, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)

    objects = managers.UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return '{}'.format(self.email)

    def get_absolute_url(self):
        return '/users/%s/' % urlquote(self.email)

    def get_full_name(self):
        """Returns the first + last name."""
        return '{} {}'.format(self.first_name, self.last_name).strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """Sends an email to this User. """
        send_mail(subject, message, from_email, [self.email])

    @property
    def primary_email(self):
        """Return the primary email associated with this User"""
        return self.email

    def create_account(self):
        """
        Called in the post-save signal, this method is responsible for
        creating an account for this ``User``. It checks that an :account:
        attribute is not present and that the user is neither a staff
        member nor a superuser.
        """
        if not hasattr(self, 'account') and not (self.is_staff or self.is_superuser):
            self.account = UserAccount.objects.create(user=self)
            self.save()

    def create_profile(self):
        """
        Called in the post-save signal, this method creates a profile for
        all new users including staff members and superusers.
        """
        if not hasattr(self, 'profile'):
            self.profile = Profile.objects.create(user=self)
            self.save()


class Profile(ContentBase):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    nickname = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.user.__str__()


class Permission(ModelBase):
    pass


class Role(ModelBase):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    organization = models.ForeignKey('organizations.Organization',
                                     related_name='roles',
                                     null=True, blank=True)
    permissions = models.ManyToManyField(Permission, related_name='roles_i_belong_to',
                                         null=True, blank=True)
    users = models.ForeignKey(User, related_name='role', null=True, blank=True)

    class Meta:
        unique_together = (('name',), ('name', 'organization'))

    def __str__(self):
        return '{} - {}'.format(self.name, self.organization)
