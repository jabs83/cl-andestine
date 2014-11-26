from django.utils.translation import ugettext_lazy as _


default_app_config = 'coachlogix.apps.organizations.apps.OrganizationAppConfig'


INVITED = 0
PENDING = 1
CREATED = 2
DISABLED = 3
REMOVED = 4
STATUS_CHOICES = (
    (INVITED, _('Invited')),
    (PENDING, _('Pending')),
    (CREATED, _('Created')),
    (DISABLED, _('Disabled')),
    (REMOVED, _('Removed')),
)
